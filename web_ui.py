#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web UI for Telegram Export Parser (requires Flask)
Install: pip install flask
"""

import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
import tempfile
from typing import Dict, Any, List

from utils import ensure_dir, unique_output_path
from exporters import get_exporter
from stats import MessageStats
from filters import MessageFilter

logger = logging.getLogger("telegram_export_parser")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max upload

# Store uploaded data in session
uploaded_data: Dict[str, Any] = {}


@app.route("/")
def index():
    """Render main page."""
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Handle file upload."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith(".json"):
            return jsonify({"error": "Only JSON files are allowed"}), 400

        # Read and parse JSON
        data = json.loads(file.read().decode("utf-8"))

        # Extract chats info
        chats_info = []
        if isinstance(data, dict) and "messages" in data:
            # Single chat export
            chats_info.append(
                {
                    "name": data.get("name", "Unknown"),
                    "message_count": len(data.get("messages", [])),
                }
            )
        else:
            # Multiple chats
            chats_root = data.get("chats", {})
            for chat in chats_root.get("list", []):
                chats_info.append(
                    {
                        "name": chat.get("name", "Unknown"),
                        "message_count": len(chat.get("messages", [])),
                    }
                )

        # Store data
        global uploaded_data
        uploaded_data = {
            "data": data,
            "chats": chats_info,
            "upload_time": str(Path.cwd()),
        }

        return jsonify(
            {"success": True, "chats": chats_info, "total_chats": len(chats_info)}
        )

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chats", methods=["GET"])
def get_chats():
    """Get list of available chats."""
    if not uploaded_data:
        return jsonify({"error": "No file uploaded"}), 400

    return jsonify({"chats": uploaded_data.get("chats", [])})


@app.route("/api/stats/<int:chat_index>", methods=["GET"])
def get_stats(chat_index: int):
    """Get statistics for a specific chat."""
    if not uploaded_data:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        data = uploaded_data["data"]
        chats = uploaded_data["chats"]

        if chat_index >= len(chats):
            return jsonify({"error": "Chat not found"}), 404

        # Get the chat data
        if isinstance(data, dict) and "messages" in data:
            chat_data = data
        else:
            chats_root = data.get("chats", {})
            chat_data = chats_root.get("list", [])[chat_index]

        # Calculate stats
        stats = MessageStats(chat_data.get("messages", []))

        return jsonify(
            {
                "total_messages": stats.get_total_messages(),
                "avg_message_length": stats.get_average_message_length(),
                "top_talkers": dict(stats.get_top_talkers(5)),
                "top_words": dict(stats.get_word_frequency(10)),
                "daily_avg": (
                    sum(stats.get_daily_message_count().values())
                    / len(stats.get_daily_message_count())
                    if stats.get_daily_message_count()
                    else 0
                ),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/export", methods=["POST"])
def export_data():
    """Export chat data in specified format."""
    if not uploaded_data:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        params = request.json
        chat_index = params.get("chat_index", 0)
        export_format = params.get("format", "csv")
        chat_name = params.get("chat_name", "export")

        if export_format not in ["txt", "csv", "json", "md", "html", "xlsx"]:
            return jsonify({"error": "Invalid format"}), 400

        # Get chat data
        data = uploaded_data["data"]
        if isinstance(data, dict) and "messages" in data:
            chat_data = data
        else:
            chats_root = data.get("chats", {})
            chat_data = chats_root.get("list", [])[chat_index]

        # Export
        exporter_class = get_exporter(export_format)
        messages = chat_data.get("messages", [])
        id_index = {str(m.get("id")): m for m in messages}
        exporter = exporter_class(messages, id_index)

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=f".{export_format}",
            delete=False,
            encoding="utf-8",
            dir=tempfile.gettempdir(),
        ) as f:
            temp_path = Path(f.name)

        exporter.export(temp_path)

        # Record generated files to avoid arbitrary file downloads
        uploaded_data.setdefault("temp_files", []).append(str(temp_path))

        return jsonify(
            {"success": True, "file": str(temp_path), "format": export_format}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download/<path:filename>", methods=["GET"])
def download_file(filename: str):
    """Download exported file."""
    try:
        allowed = uploaded_data.get("temp_files", [])
        requested = str(Path(filename))
        if requested not in allowed:
            return jsonify({"error": "Unauthorized or unknown file"}), 403

        file_path = Path(requested)
        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"telegram_export{file_path.suffix}",
        )
    except Exception as e:
        logger.exception("Error in download_file")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info("🌐 Starting Telegram Export Parser Web UI...")
    logger.info("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, host="0.0.0.0", port=5000)
