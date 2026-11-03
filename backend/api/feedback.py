# backend/api/feedback.py
"""Feedback endpoint – email only (no database).

The endpoint validates the payload, sends a notification e‑mail in a background
task, and optionally logs the request to a local JSON file (a very cheap
fallback).  No database engine is required.
"""

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
import os, json, datetime, smtplib, ssl
from email.message import EmailMessage
from pathlib import Path

router = APIRouter(prefix="/feedback", tags=["feedback"])

# ----------------------------------------------------------------------
# Request payload – same as before so the UI does not need to change.
# ----------------------------------------------------------------------
class Feedback(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    rating: int = Field(..., ge=1, le=5, description="1‑5 star rating")
    comment: str = Field(..., example="Great app, but …")

# ----------------------------------------------------------------------
# Background e‑mail sender.
# ----------------------------------------------------------------------
def _send_email(fb: Feedback):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port   = int(os.getenv("SMTP_PORT", "465"))
    smtp_user   = os.getenv("SMTP_USER")
    smtp_pass   = os.getenv("SMTP_PASS")
    to_addr     = os.getenv("FEEDBACK_RECEIVER")

    # If any variable missing, skip sending – the endpoint still succeeds.
    if not all([smtp_server, smtp_user, smtp_pass, to_addr]):
        return

    msg = EmailMessage()
    msg["Subject"] = f"🗣️ New Feedback from {fb.name}"
    msg["From"]    = smtp_user
    msg["To"]      = to_addr
    msg.set_content(
        f"""You have received a new feedback submission:\n\n"
        f"Name   : {fb.name}\n"
        f"Email  : {fb.email}\n"
        f"Rating : {fb.rating} / 5\n\n"
        f"Comment:\n{fb.comment}\n"""
    )
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ctx) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

# ----------------------------------------------------------------------
# Optional lightweight flat‑file logger – useful if you want a local copy.
# ----------------------------------------------------------------------
def _append_to_log_file(fb: Feedback):
    log_path = Path("feedback_log.json")
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "name": fb.name,
        "email": fb.email,
        "rating": fb.rating,
        "comment": fb.comment,
    }
    if log_path.is_file():
        try:
            data = json.loads(log_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []
    else:
        data = []
    data.append(entry)
    log_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

# ----------------------------------------------------------------------
# POST endpoint – send e‑mail (if enabled) and log to JSON.
# ----------------------------------------------------------------------
@router.post("/", status_code=202)
async def submit_feedback(feedback: Feedback, background_tasks: BackgroundTasks):
    """Receive a feedback payload, fire a background e‑mail, and log locally.

    The e‑mail is sent only when ``ENABLE_FEEDBACK_EMAIL`` is truthy.
    """
    if os.getenv("ENABLE_FEEDBACK_EMAIL", "true").lower() == "true":
        background_tasks.add_task(_send_email, feedback)
    # Always log to a simple JSON file – cheap and requires no DB.
    background_tasks.add_task(_append_to_log_file, feedback)
    return {"detail": "Feedback received – thank you!"}

