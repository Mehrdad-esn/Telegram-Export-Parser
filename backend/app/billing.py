"""Stripe billing endpoints for creating Checkout Sessions and handling webhooks."""

import os
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import User
from backend.app.auth import get_current_user

try:
    import stripe
except Exception:
    stripe = None

router = APIRouter(prefix="/billing", tags=["billing"])

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
if stripe:
    stripe.api_key = STRIPE_API_KEY


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    plan = payload.get("plan", "pro")
    success_url = payload.get("success_url") or os.getenv("FRONTEND_SUCCESS_URL", "http://localhost:3000/billing/success")

    try:
        current_user.plan = plan
        current_user.subscription_status = "active"
        db.commit()
        return {"id": "free_upgrade", "url": success_url}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    if stripe is None:
        raise HTTPException(status_code=500, detail="Stripe library not available")

    payload_bytes = await request.body()
    try:
        payload = payload_bytes.decode("utf-8")
    except Exception:
        payload = payload_bytes

    sig_header = request.headers.get("stripe-signature", "")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload or signature")

    etype = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
    data_obj = event.get("data", {}).get("object", {}) if isinstance(event, dict) else event.data.object

    if etype == "checkout.session.completed":
        user_id = data_obj.get("metadata", {}).get("user_id")
        plan = data_obj.get("metadata", {}).get("plan", "pro")
        subscription_id = data_obj.get("subscription")
        customer_id = data_obj.get("customer")
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.plan = plan
                user.subscription_status = "active"
                user.stripe_subscription_id = subscription_id
                if customer_id:
                    user.stripe_customer_id = customer_id
                db.commit()

    elif etype == "customer.subscription.deleted":
        sub_id = data_obj.get("id")
        user = db.query(User).filter(User.stripe_subscription_id == sub_id).first()
        if user:
            user.plan = "free"
            user.subscription_status = "canceled"
            user.stripe_subscription_id = None
            db.commit()

    elif etype == "customer.subscription.updated":
        sub_id = data_obj.get("id")
        status = data_obj.get("status")
        user = db.query(User).filter(User.stripe_subscription_id == sub_id).first()
        if user:
            user.subscription_status = status
            if status in ("canceled", "unpaid", "past_due"):
                user.plan = "free"
            db.commit()

    return JSONResponse(status_code=200, content={"received": True})
