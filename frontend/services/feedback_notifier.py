import os
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

CREATOR_EMAIL = "mogiliadieshwarreddy5919@gmail.com"

def save_feedback_local(entry: dict) -> bool:
    """Save feedback locally to database/feedback_submissions.json."""
    try:
        feedback_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database"))
        os.makedirs(feedback_dir, exist_ok=True)
        feedback_file = os.path.join(feedback_dir, "feedback_submissions.json")
        
        submissions = []
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, "r", encoding="utf-8") as f:
                    submissions = json.load(f)
            except Exception:
                submissions = []
                
        submissions.append(entry)
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def save_feedback_supabase(entry: dict) -> bool:
    """Optional: save feedback to Supabase if credentials are present."""
    try:
        import streamlit as st
        supabase_url = st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None
        supabase_key = st.secrets.get("SUPABASE_ANON_KEY") if hasattr(st, "secrets") else None
        
        if not supabase_url:
            supabase_url = os.getenv("SUPABASE_URL")
        if not supabase_key:
            supabase_key = os.getenv("SUPABASE_ANON_KEY")
            
        if supabase_url and supabase_key:
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            res = requests.post(
                f"{supabase_url.rstrip('/')}/rest/v1/feedback",
                headers=headers,
                json=entry,
                timeout=5
            )
            return res.status_code in (200, 201, 204)
    except Exception:
        pass
    return False

def send_feedback_smtp(entry: dict) -> bool:
    """Send feedback email notification to creator via SMTP if configured."""
    try:
        import streamlit as st
        def get_setting(key, default=""):
            val = None
            if hasattr(st, "secrets"):
                try:
                    val = st.secrets.get(key)
                except Exception:
                    pass
            if not val:
                val = os.getenv(key, default)
            return val

        smtp_user = get_setting("SMTP_USER") or get_setting("SENDER_EMAIL")
        smtp_pass = get_setting("SMTP_PASSWORD") or get_setting("EMAIL_APP_PASSWORD")
        smtp_host = get_setting("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(get_setting("SMTP_PORT", "587"))
        dest_email = get_setting("NOTIFICATION_EMAIL", CREATOR_EMAIL)

        if not smtp_user or not smtp_pass:
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚀 New Feedback Received on Adhii ATS Resume [{entry.get('rating', 'Feedback')}]"
        msg["From"] = f"Adhii ATS Resume <{smtp_user}>"
        msg["To"] = dest_email
        if entry.get("email"):
            msg["Reply-To"] = entry.get("email")

        text_body = f"""New User Feedback Received for Adhii ATS Resume:
--------------------------------------------------------
Rating:      {entry.get('rating')}
Submitted By: {entry.get('name') or 'Anonymous User'}
User Email:   {entry.get('email') or 'Not provided'}
Timestamp:    {entry.get('timestamp')}

Comments & Suggestions:
{entry.get('comments')}
--------------------------------------------------------
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 24px; color: #1e293b;">
    <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="background: linear-gradient(135deg, #2563EB, #7C3AED); padding: 20px 24px; color: #ffffff;">
            <h2 style="margin: 0; font-size: 20px;">🚀 New Feedback Received</h2>
            <p style="margin: 4px 0 0; opacity: 0.9; font-size: 13px;">Adhii ATS Resume Platform</p>
        </div>
        <div style="padding: 24px;">
            <div style="margin-bottom: 16px; padding: 12px 16px; background: #f1f5f9; border-radius: 8px;">
                <p style="margin: 4px 0;"><strong>⭐ Experience Rating:</strong> {entry.get('rating')}</p>
                <p style="margin: 4px 0;"><strong>👤 User:</strong> {entry.get('name') or 'Anonymous'}</p>
                <p style="margin: 4px 0;"><strong>✉️ Email:</strong> {entry.get('email') or 'Not provided'}</p>
                <p style="margin: 4px 0; font-size: 12px; color: #64748b;"><strong>🕒 Date:</strong> {entry.get('timestamp')}</p>
            </div>
            <div style="margin-top: 16px;">
                <h4 style="margin: 0 0 8px; color: #0f172a;">📝 Comments & Suggestions:</h4>
                <div style="background: #fafafa; border-left: 4px solid #3b82f6; padding: 12px 16px; font-size: 14px; line-height: 1.6; white-space: pre-wrap;">{entry.get('comments')}</div>
            </div>
        </div>
    </div>
</body>
</html>"""

        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        return True
    except Exception:
        return False

def send_feedback_webhook(entry: dict) -> bool:
    """Send feedback via Web3Forms or custom webhook if configured."""
    try:
        import streamlit as st
        def get_setting(key):
            val = None
            if hasattr(st, "secrets"):
                try:
                    val = st.secrets.get(key)
                except Exception:
                    pass
            if not val:
                val = os.getenv(key)
            return val

        # 1. Web3Forms support (Free form-to-email service)
        web3forms_key = get_setting("WEB3FORMS_ACCESS_KEY")
        if web3forms_key:
            payload = {
                "access_key": web3forms_key,
                "subject": f"🚀 New Feedback: Adhii ATS Resume ({entry.get('rating')})",
                "from_name": entry.get("name") or "Adhii ATS User",
                "email": entry.get("email") or CREATOR_EMAIL,
                "message": f"Rating: {entry.get('rating')}\nUser: {entry.get('name')}\nEmail: {entry.get('email')}\n\nFeedback:\n{entry.get('comments')}",
                "to_email": CREATOR_EMAIL
            }
            res = requests.post("https://api.web3forms.com/submit", json=payload, timeout=8)
            if res.status_code == 200:
                return True

        # 2. Custom Webhook (e.g. Discord, Slack, Zapier, Formspree)
        webhook_url = get_setting("FEEDBACK_WEBHOOK_URL")
        if webhook_url:
            payload = {
                "content": f"**New Feedback on Adhii ATS Resume**\n• Rating: {entry.get('rating')}\n• From: {entry.get('name') or 'Anonymous'} ({entry.get('email') or 'N/A'})\n• Comments: {entry.get('comments')}"
            }
            res = requests.post(webhook_url, json=payload, timeout=8)
            if res.status_code in (200, 201, 204):
                return True
    except Exception:
        pass
    return False

def submit_feedback(rating: str, comments: str, name: str = "", email: str = "") -> dict:
    """
    Submits user feedback through all available channels:
    1. Local database persistence
    2. Supabase storage (if configured)
    3. Direct SMTP email to creator (if configured)
    4. Webhook / Web3Forms email delivery (if configured)
    """
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name.strip(),
        "email": email.strip(),
        "rating": rating,
        "comments": comments.strip()
    }

    local_ok = save_feedback_local(entry)
    supabase_ok = save_feedback_supabase(entry)
    smtp_ok = send_feedback_smtp(entry)
    webhook_ok = send_feedback_webhook(entry)

    email_sent = smtp_ok or webhook_ok

    return {
        "success": local_ok or supabase_ok or email_sent,
        "email_sent": email_sent,
        "local_saved": local_ok,
        "supabase_saved": supabase_ok
    }

