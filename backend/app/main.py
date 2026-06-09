from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List

# Ensure repo root is importable so we can reuse parsing logic without moving files.
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Try to import processor module from backend.app. Fall back to previous helpers if missing.
processor = None
try:
    from backend.app import processor  # type: ignore
except Exception:
    processor = None
    try:
        from telegram_to_text import format_message, build_id_index  # type: ignore
    except Exception:
        format_message = None
        build_id_index = None

app = FastAPI(title="Telegram Export Parser Backend")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/process")
async def process(request: Request) -> Dict[str, Any]:
    """Accept either a multipart/form-data upload (field name 'file') or
    an application/json body containing either a single chat object
    (with 'messages') or an export root (with 'chats': {'list': [...] }).

    This endpoint runs synchronously and returns the processed chat text
    in a JSON structure. For long-running workloads, move processing to
    a background task or queue (TODO).
    """
    try:
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("multipart/form-data"):
            form = await request.form()
            upload = form.get("file")
            if upload is None:
                raise HTTPException(status_code=400, detail="No file field in form data")
            contents = await upload.read()
            data = json.loads(contents.decode("utf-8"))
        else:
            data = await request.json()

        # Prefer processor module if available
        if processor:
            try:
                # processor supports payload processing; prefer in-memory payload
                return processor.process_export_from_payload(data)
            except Exception as e:
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(e))

        # Fallback: inline processing (kept for backwards compatibility)
        def iter_chats_from_data(obj: Any):
            if isinstance(obj, dict) and "messages" in obj:
                yield obj
            else:
                chats_root = obj.get("chats", {}) if isinstance(obj, dict) else {}
                for chat in chats_root.get("list", []):
                    yield chat

        result_chats: List[Dict[str, Any]] = []
        for chat in iter_chats_from_data(data):
            chat_name = chat.get("name") or "Unnamed chat"
            messages = chat.get("messages") or []
            if not isinstance(messages, list):
                messages = []

            # Build id index (simple local implementation to avoid hard dependency)
            id_index = {}
            for m in messages:
                if isinstance(m, dict) and m.get("id") is not None:
                    id_index[str(m.get("id"))] = m

            formatted_messages: List[str] = []
            for m in messages:
                if not isinstance(m, dict) or m.get("type") != "message":
                    continue
                if format_message:
                    try:
                        fm = format_message(m, id_index)
                    except Exception:
                        # fallback
                        ts = m.get("date", "").replace("T", " ")
                        sender = m.get("from") or m.get("actor") or m.get("author") or "Unknown"
                        text_field = m.get("text")
                        if isinstance(text_field, str):
                            text = text_field
                        else:
                            text = json.dumps(text_field, ensure_ascii=False) if text_field is not None else ""
                        fm = f"[{ts}] {sender}\n{text}"
                else:
                    ts = m.get("date", "").replace("T", " ")
                    sender = m.get("from") or m.get("actor") or m.get("author") or "Unknown"
                    text_field = m.get("text")
                    if isinstance(text_field, str):
                        text = text_field
                    else:
                        text = json.dumps(text_field, ensure_ascii=False) if text_field is not None else ""
                    fm = f"[{ts}] {sender}\n{text}"

                formatted_messages.append(fm)

            result_chats.append({"name": chat_name, "messages": formatted_messages})

        return {"processed": True, "chats": result_chats}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


# Include auth router and ensure database tables are created
try:
    from backend.app import auth as _auth_module
    app.include_router(_auth_module.router)
except Exception as _e:
    print("Auth module not loaded:", _e)

try:
    # Ensure models are imported and tables created
    from backend.app import models as _models
    from backend.app.db import Base as _Base, engine as _engine
    _Base.metadata.create_all(bind=_engine)
except Exception as _e:
    print("Could not create database tables:", _e)
