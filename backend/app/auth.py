"""Authentication utilities: signup, login, refresh, and current_user dependency."""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.orm import Session

from config import Config
from backend.app.db import get_db
from backend.app.models import User
from backend.app.subscription import get_usage_summary, PLANS

config = Config()
SECRET_KEY = os.getenv("SECRET_KEY", config.get_secret_key())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
optional_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/api", tags=["auth"])


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    plan: str = "free"
    subscription_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    plan: str
    subscription_status: Optional[str] = None
    usage: dict
    plans: dict


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt has a 72 byte password length limit; pre-hash long passwords with sha256
    import hashlib

    raw = plain_password if isinstance(plain_password, str) else str(plain_password)
    if len(raw.encode("utf-8")) > 72:
        raw = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return pwd_context.verify(raw, hashed_password)


def get_password_hash(password: str) -> str:
    import hashlib

    raw = password if isinstance(password, str) else str(password)
    if len(raw.encode("utf-8")) > 72:
        raw = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return pwd_context.hash(raw)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def _create_token(subject: str, expires_delta: Optional[timedelta]) -> str:
    import time

    to_encode = {"sub": subject}
    # Use time.time() for epoch seconds to avoid potential datetime timezone issues
    expires_in = int(expires_delta.total_seconds()) if expires_delta is not None else ACCESS_TOKEN_EXPIRE_MINUTES * 60
    to_encode.update({"exp": int(time.time()) + expires_in})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    return _create_token(subject, expires_delta if expires_delta is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    return _create_token(subject, expires_delta if expires_delta is not None else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))


class GuestUser:
    def __init__(self):
        self.id = 0
        self.email = "guest@example.com"
        self.is_active = True
        self.is_superuser = False
        self.plan = "free"
        self.subscription_status = "active"
        self.uploads_this_month = 0
        self.exports_this_month = 0
        self.last_usage_reset = None


oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)


def get_current_user_or_guest(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
):
    if not token:
        return GuestUser()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return GuestUser()
    except JWTError:
        return GuestUser()
    user = get_user_by_email(db, email)
    if not user:
        return GuestUser()
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if credentials is None:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return get_user_by_email(db, email)
    except JWTError:
        return None



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if not user:
        raise credentials_exception
    return user


@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(payload: dict, db: Session = Depends(get_db)):
    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    try:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=UserProfile)
def read_profile(current_user: User = Depends(get_current_user)):
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        plan=current_user.plan or "free",
        subscription_status=current_user.subscription_status,
        usage=get_usage_summary(current_user),
        plans={k: {"name": v["name"], "name_en": v["name_en"], "price_monthly": v["price_monthly"]} for k, v in PLANS.items()},
    )
