import streamlit as st
import os, json, datetime, smtplib, ssl
from email.message import EmailMessage

# -------------------------------------------------
# Load environment variables (Streamlit reads .env automatically)
# -------------------------------------------------
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT   = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASS")
FEEDBACK_RECEIVER = os.getenv("FEEDBACK_RECEIVER")
ENABLE_FEEDBACK_EMAIL = os.getenv("ENABLE_FEEDBACK_EMAIL", "true").lower() == "true"

# -------------------------------------------------
# Helper – send e‑mail (runs synchronously, but it’s fast)
# -------------------------------------------------
def send_email(name: str, email: str, rating: int, comment: str) -> bool:
    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASS, FEEDBACK_RECEIVER]):
        return False
    msg = EmailMessage()
    msg["Subject"] = f"🗣️ New Feedback from {name}"
    msg["From"]    = SMTP_USER
    msg["To"]      = FEEDBACK_RECEIVER
    msg.set_content(
        f"""You have received a new feedback submission:\n\n"
        f"Name   : {name}\n"
        f"Email  : {email}\n"
        f"Rating : {rating} / 5\n\n"
        f"Comment:\n{comment}\n"""
    )
    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ctx) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"⚠️ Email sending failed: {e}")
        return False

# -------------------------------------------------
# Helper – log to a local JSON file (optional persistence)
# -------------------------------------------------
def log_to_file(name: str, email: str, rating: int, comment: str):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "name": name,
        "email": email,
        "rating": rating,
        "comment": comment,
    }
    log_path = "feedback_log.json"
    try:
        if os.path.isfile(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        else:
            data = []
    except Exception:
        data = []
    data.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.title("📨 Give us your feedback")
st.write(
    """
    We’d love to hear what you think!  
    Fill the form below – we’ll send a notification e‑mail and store a copy locally.
    """
)

with st.form(key="feedback_form"):
    name = st.text_input("Your name", max_chars=50)
    email = st.text_input("Your e‑mail", type="email")
    rating = st.slider("How do you rate the app?", 1, 5, 5)
    comment = st.text_area("Comments / suggestions", height=150)

    submitted = st.form_submit_button("Send Feedback")

if submitted:
    if not (name and email and comment):
        st.error("All fields are required.")
    else:
        # Log locally (always)
        log_to_file(name, email, rating, comment)
        # Send e‑mail if enabled
        if ENABLE_FEEDBACK_EMAIL:
            if send_email(name, email, rating, comment):
                st.success("✅ Thank you! Your feedback has been recorded and emailed.")
            else:
                st.warning("✅ Feedback saved locally, but e‑mail could not be sent.")
        else:
            st.success("✅ Feedback saved locally (e‑mail disabled).")
