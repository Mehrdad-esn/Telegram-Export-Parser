import json
import uuid
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

import sys
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from stats import MessageStats
from exporters import get_exporter
from filters import MessageFilter
from backend.app.auth import get_current_user_or_guest
from backend.app.db import get_db
from backend.app.models import User
from backend.app.subscription import check_upload_allowed, check_export_allowed, get_plan_limits

router = APIRouter(prefix="/api/web", tags=["web_ui"])

UPLOAD_DIR = Path(tempfile.gettempdir()) / "telegram_parser_uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB absolute max


class ExportRequest(BaseModel):
    chat_index: int
    format: str
    filters: Optional[Dict[str, Any]] = None


class FilterRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    senders: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    keyword_mode: str = "any"
    regex: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    has_media: Optional[bool] = None


def get_upload_path(upload_id: str) -> Path:
    return UPLOAD_DIR / f"{upload_id}.json"


def get_export_dir(upload_id: str) -> Path:
    export_dir = UPLOAD_DIR / f"{upload_id}_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def parse_chats_info(data: Dict) -> List[Dict[str, Any]]:
    chats_info = []
    if isinstance(data, dict) and "messages" in data:
        chats_info.append({
            "name": data.get("name", "Unknown"),
            "message_count": len(data.get("messages", [])),
        })
    else:
        chats_root = data.get("chats", {})
        for chat in chats_root.get("list", []):
            chats_info.append({
                "name": chat.get("name", "Unknown"),
                "message_count": len(chat.get("messages", [])),
            })
    return chats_info


def get_chat_data(data: Dict, chat_index: int) -> Dict[str, Any]:
    if isinstance(data, dict) and "messages" in data:
        if chat_index != 0:
            raise ValueError("Invalid chat index for single-chat export")
        return data
    chats_root = data.get("chats", {})
    chat_list = chats_root.get("list", [])
    if chat_index < 0 or chat_index >= len(chat_list):
        raise ValueError("Chat index out of range")
    return chat_list[chat_index]


def apply_filters(messages: List[Dict], filters: Optional[Dict[str, Any]]) -> List[Dict]:
    if not filters:
        return messages
    mf = MessageFilter(messages)
    if filters.get("start_date") or filters.get("end_date"):
        mf.add_date_range(filters.get("start_date"), filters.get("end_date"))
    if filters.get("senders"):
        mf.add_sender_filter(filters["senders"])
    if filters.get("keywords"):
        mf.add_keyword_filter(filters["keywords"], filters.get("keyword_mode", "any"))
    if filters.get("regex"):
        mf.add_regex_filter(filters["regex"])
    if filters.get("min_length") or filters.get("max_length"):
        mf.add_length_filter(filters.get("min_length"), filters.get("max_length"))
    if filters.get("has_media") is not None:
        mf.add_has_media_filter(filters["has_media"])
    return mf.apply()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_or_guest),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")

    err = check_upload_allowed(current_user)
    if err:
        raise HTTPException(status_code=403, detail=err)

    limits = get_plan_limits(current_user.plan or "free")
    max_size = limits["max_file_size_mb"] * 1024 * 1024

    upload_id = str(uuid.uuid4())
    file_path = get_upload_path(upload_id)

    try:
        size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    file_path.unlink(missing_ok=True)
                    raise HTTPException(status_code=413, detail="File too large")
                if size > max_size:
                    file_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"حداکثر حجم فایل در پلن شما {limits['max_file_size_mb']}MB است",
                    )
                buffer.write(chunk)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chats_info = parse_chats_info(data)
        max_chats = limits.get("max_chats")
        if max_chats and len(chats_info) > max_chats:
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=403,
                detail=f"پلن شما حداکثر {max_chats} چت را پشتیبانی می‌کند",
            )

        if current_user.id != 0:
            current_user.uploads_this_month += 1
            db.commit()

        return {
            "success": True,
            "upload_id": upload_id,
            "total_chats": len(chats_info),
            "chats": chats_info,
        }
    except json.JSONDecodeError:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except HTTPException:
        raise
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chats/{upload_id}")
async def get_chats(upload_id: str, current_user: User = Depends(get_current_user_or_guest)):
    file_path = get_upload_path(upload_id)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Upload not found or expired")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"chats": parse_chats_info(data)}


@router.get("/stats/{upload_id}/{chat_index}")
async def get_stats(
    upload_id: str,
    chat_index: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    senders: Optional[str] = None,
    keywords: Optional[str] = None,
    current_user: User = Depends(get_current_user_or_guest),
):
    file_path = get_upload_path(upload_id)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Upload not found or expired")

    filters = {}
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date
    if senders:
        filters["senders"] = [s.strip() for s in senders.split(",") if s.strip()]
    if keywords:
        filters["keywords"] = [k.strip() for k in keywords.split(",") if k.strip()]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chat_data = get_chat_data(data, chat_index)
        messages = chat_data.get("messages", [])
        filtered = apply_filters(messages, filters if filters else None)

        stats = MessageStats(filtered)
        daily_counts = stats.get_daily_message_count()
        daily_avg = sum(daily_counts.values()) / len(daily_counts) if daily_counts else 0
        timeline = [{"date": k, "messages": v} for k, v in sorted(daily_counts.items())]
        top_talkers_raw = stats.get_top_talkers(10)
        top_talkers_chart = [{"name": name, "count": count} for name, count in top_talkers_raw]

        from utils import extract_sender_name
        all_senders = sorted({extract_sender_name(m) for m in messages if m.get("type") == "message"})

        return {
            "total_messages": stats.get_total_messages(),
            "filtered_messages": len(filtered),
            "total_unfiltered": len([m for m in messages if m.get("type") == "message"]),
            "avg_message_length": stats.get_average_message_length(),
            "top_talkers": dict(top_talkers_raw),
            "top_talkers_chart": top_talkers_chart,
            "top_words": dict(stats.get_word_frequency(15)),
            "daily_avg": daily_avg,
            "timeline": timeline,
            "available_senders": all_senders,
            "filters_applied": bool(filters),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/{upload_id}")
async def export_data(
    upload_id: str,
    req: ExportRequest,
    current_user: User = Depends(get_current_user_or_guest),
    db: Session = Depends(get_db),
):
    file_path = get_upload_path(upload_id)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Upload not found or expired")

    fmt = req.format.lower()
    if fmt not in ["txt", "csv", "json", "md", "html", "xlsx", "excel"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    err = check_export_allowed(current_user, fmt)
    if err:
        raise HTTPException(status_code=403, detail=err)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chat_data = get_chat_data(data, req.chat_index)
        messages = chat_data.get("messages", [])
        filtered = apply_filters(messages, req.filters)

        id_index = {str(m.get("id")): m for m in messages if m.get("id")}
        exporter_class = get_exporter(fmt)
        exporter = exporter_class(filtered, id_index)

        export_dir = get_export_dir(upload_id)
        safe_chat_name = "".join(
            [c for c in chat_data.get("name", "chat") if c.isalpha() or c.isdigit() or c == " "]
        ).rstrip() or "chat"

        ext = "xlsx" if fmt in ["excel", "xlsx"] else fmt
        output_filename = f"{safe_chat_name}_export.{ext}"
        output_path = export_dir / output_filename

        if output_path.exists():
            output_filename = f"{safe_chat_name}_{uuid.uuid4().hex[:6]}.{ext}"
            output_path = export_dir / output_filename

        exporter.export(output_path)

        if current_user.id != 0:
            current_user.exports_this_month += 1
            db.commit()

        return {
            "success": True,
            "file_id": f"{upload_id}/{output_filename}",
            "format": fmt,
            "message_count": len(filtered),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{upload_id}/{filename}")
async def download_file(
    upload_id: str,
    filename: str,
):
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    export_dir = get_export_dir(upload_id)
    file_path = export_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )
