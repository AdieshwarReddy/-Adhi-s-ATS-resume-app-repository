# ATS Resume Feedback App (End‑to‑End Guide)
**#DEPLOYED LINK : https://adhisatsresumeapp.streamlit.app/**
## Overview
This small project demonstrates a **FastAPI backend** that receives user feedback, stores it in a SQLite database, and (optionally) sends you an email notification. A **Streamlit front‑end** provides a browser‑friendly form that works on any modern browser. The whole stack can be run locally or deployed to a cloud host.

---

## 📁 Project Structure
```
ATS Resume/
├─ backend/                     # FastAPI server
│   ├─ api/                     # API routers
│   │   ├─ auth.py              # (existing auth example)
│   │   ├─ history.py           # (existing history example)
│   │   ├─ feedback.py          # NEW – feedback endpoint
│   │   ├─ feedback_admin.py    # OPTIONAL – admin view (protected)
│   │   └─ models.py            # NEW – SQLAlchemy model
│   ├─ db.py                    # NEW – DB engine & session helper
│   └─ main.py                  # FastAPI app entry point (include routers)
├─ frontend/                    # Streamlit UI
│   └─ feedback_app.py          # NEW – simple feedback form
├─ .env                         # Environment variables (kept out of VCS)
├─ requirements.txt             # Python deps (FastAPI, Streamlit, SQLAlchemy…)
└─ README.md                    # **You are reading it**
```

---

## 🔧 Prerequisites
- **Python 3.10+** (recommended 3.12)
- **Git** (for version control)
- An SMTP account (e.g., Gmail app‑password) if you want e‑mail notifications.
- (Optional) Docker if you plan to containerise the app.

---

## 1️⃣ Setup the Development Environment
```powershell
# 1. Clone the repo (skip if you already have the folder)
# git clone <repo‑url>
# cd "c:\Adhi's ATS Resume"

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell
# or `venv\Scripts\activate.bat` for cmd

# 3. Install dependencies
pip install -r requirements.txt
# plus the new ones for the DB layer
pip install sqlalchemy aiosqlite
```

---

## 2️⃣ Configure Secrets (`.env`)
Create a file named **`.env`** in the project root (it is already ignored by Git). Add the following keys and replace the placeholder values with your own:
```dotenv
# ---------- Email configuration (optional) ----------
SMTP_SERVER=smtp.gmail.com          # or your provider
SMTP_PORT=465
SMTP_USER=your@email.com
SMTP_PASS=your_app_password        # Gmail → App Password
FEEDBACK_RECEIVER=your@email.com   # where you want to receive feedback

# ---------- Database ----------
# SQLite (default) – stored as `feedback.db` in the repo root
DATABASE_URL=sqlite+aiosqlite:///./feedback.db

# ---------- Feature switches ----------
# Set to "false" if you only want DB storage and no email notifications
ENABLE_FEEDBACK_EMAIL=true
```
> **Security tip:** Never commit `.env` to any public repository. It is already listed in `.gitignore`.

---

## 3️⃣ Run the FastAPI Backend
```powershell
# From the project root
uvicorn backend.main:app --reload
```
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```
The first request will automatically create `feedback.db` and the `feedback` table.

---

## 4️⃣ Run the Streamlit Front‑End
Open **another** terminal (keep the backend running) and execute:
```powershell
streamlit run frontend\feedback_app.py
```
A browser tab opens (usually `http://localhost:8501`). Fill the form and click **Send Feedback**.
- If everything is configured, you’ll see a **✅ Thanks!** message.
- If `ENABLE_FEEDBACK_EMAIL` is `true`, you’ll also receive an email with the same data.

---

## 5️⃣ Verify the Feedback was Stored
You can inspect the SQLite file directly:
```powershell
sqlite3 feedback.db "SELECT id, name, rating, created_at FROM feedback ORDER BY id DESC LIMIT 5;"
```
You should see rows corresponding to the submissions you made via Streamlit.

---

## 6️⃣ (Optional) Admin Endpoint
If you want a quick JSON view of all feedback entries, you can enable the admin router:
1. Add the router in `backend/main.py`:
```python
from backend.api.feedback_admin import router as admin_router
app.include_router(admin_router)
```
2. Protect it with your existing authentication dependency (e.g., `Depends(get_current_user)`).
3. Access it at `http://127.0.0.1:8000/admin/feedback/` – it will return a JSON list.

---

## 7️⃣ Push to GitHub (one‑time)
```powershell
git init                     # if not already a repo
git add .
git commit -m "Add feedback API, DB storage, Streamlit UI"
git branch -M main
git remote add origin https://github.com/youruser/ats-resume.git
git push -u origin main
```
Your code is now version‑controlled and ready for CI/CD.

---

## 8️⃣ Deploy (quick Docker example)
Create a **Dockerfile** in the root (optional – see the previous discussion). Then run:
```powershell
docker build -t ats‑resume .
# Run backend and front‑end as separate containers or use docker‑compose.
```
Most PaaS platforms (Render, Railway, Fly.io) can build from this Dockerfile automatically.

---

## 🎉 What you have built
1. **FastAPI route** `/feedback/` that accepts a JSON payload and:
   - Persists it to a SQLite DB (`feedback.db`).
   - Sends a notification e‑mail in the background (optional).
2. **Streamlit UI** (`frontend/feedback_app.py`) – a browser‑agnostic form for users.
3. **Database layer** (`backend/db.py`, `backend/api/models.py`).
4. **Full README** (this file) that walks anyone through setup, running, testing, and deploying.

---

## 📌 Next Steps You May Want
- Switch to PostgreSQL for production (`DATABASE_URL=postgresql+asyncpg://…`).
- Add rate‑limiting / CAPTCHA to prevent spam. 
- Create a tiny admin dashboard in Streamlit that reads from the `/admin/feedback/` endpoint. 
- Set up CI with GitHub Actions to run tests on every push.

---

## 🙋‍♂️ Need More Help?
Just let me know which of the optional items you’d like to implement next, or if you hit any errors while following the steps. I can generate the missing files, adjust configuration, or walk you through a deployment to a specific cloud provider.
