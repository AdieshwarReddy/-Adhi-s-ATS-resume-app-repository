import os

def write_file(path, content):
    d=os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

files = {}

# .env.example
files['.env.example'] = """
APP_ENV=development

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

GROQ_API_KEY=
GROQ_MODEL=llama3-8b-8192

FRONTEND_URL=http://localhost:8501
BACKEND_URL=http://localhost:8000

SENTENCE_TRANSFORMER_MODEL=sentence-transformers/all-MiniLM-L6-v2
SPACY_MODEL=en_core_web_md

MAX_UPLOAD_MB=10
"""

files['frontend/.streamlit/secrets.toml.example'] = """
SUPABASE_URL=""
SUPABASE_ANON_KEY=""
BACKEND_URL="http://localhost:8000"
"""

# backend/core/config.py
files['backend/core/config.py'] = """
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-8b-8192"
    
    FRONTEND_URL: str = "http://localhost:8501"
    BACKEND_URL: str = "http://localhost:8000"
    
    SENTENCE_TRANSFORMER_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    SPACY_MODEL: str = "en_core_web_md"
    
    MAX_UPLOAD_MB: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
"""

files['backend/main.py'] = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api import routes

app = FastAPI(
    title="Adhii ATS Resume API",
    description="AI-Powered Resume Intelligence & Job Matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Adhii ATS Resume API"}
"""

files['backend/api/routes.py'] = """
from fastapi import APIRouter
from backend.api import auth, analysis, history, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(analysis.router, tags=["Analysis"])
api_router.include_router(history.router, prefix="/analyses", tags=["History"])
api_router.include_router(reports.router, prefix="/analyses", tags=["Reports"])

@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
"""

files['backend/api/auth.py'] = """
from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def get_me():
    return {"user": "current_user_placeholder"}
"""

files['backend/api/analysis.py'] = """
from fastapi import APIRouter, File, UploadFile, Form
router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(""),
    company_name: str = Form("")
):
    return {"status": "mock", "message": "Analyze endpoint ready for implementation"}
"""

files['backend/api/history.py'] = """
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_analyses():
    return []

@router.get("/{analysis_id}")
def get_analysis(analysis_id: str):
    return {"id": analysis_id}

@router.delete("/{analysis_id}")
def delete_analysis(analysis_id: str):
    return {"status": "deleted"}
"""

files['backend/api/reports.py'] = """
from fastapi import APIRouter
router = APIRouter()

@router.get("/{analysis_id}/report")
def get_report(analysis_id: str):
    return {"status": "mock", "message": "Report generation endpoint"}
"""

files['backend/database/supabase_db.py'] = """
from supabase import create_client, Client
from backend.core.config import settings

def get_supabase_client() -> Client:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
    if not url or not key:
        raise ValueError("Supabase credentials not configured properly.")
    return create_client(url, key)

db = get_supabase_client() if settings.SUPABASE_URL else None
"""

files['database/schema.sql'] = """
-- Supabase Schema Setup

CREATE TABLE profiles (
    id UUID REFERENCES auth.users NOT NULL PRIMARY KEY,
    email TEXT NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE resume_analyses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users NOT NULL,
    resume_filename TEXT,
    job_title TEXT,
    company_name TEXT,
    job_description TEXT,
    overall_score INTEGER,
    formatting_score INTEGER,
    keyword_score INTEGER,
    content_score INTEGER,
    skill_validation_score INTEGER,
    ats_compatibility_score INTEGER,
    semantic_similarity FLOAT,
    matched_skills JSONB,
    missing_skills JSONB,
    recommendations JSONB,
    feedback JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

files['database/policies.sql'] = """
-- Row Level Security (RLS) Policies

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_analyses ENABLE ROW LEVEL SECURITY;

-- Profiles Policies
CREATE POLICY "Users can view their own profile" 
ON profiles FOR SELECT 
USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" 
ON profiles FOR INSERT 
WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile" 
ON profiles FOR UPDATE 
USING (auth.uid() = id);

-- Resume Analyses Policies
CREATE POLICY "Users can view their own analyses" 
ON resume_analyses FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own analyses" 
ON resume_analyses FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own analyses" 
ON resume_analyses FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own analyses" 
ON resume_analyses FOR DELETE 
USING (auth.uid() = user_id);
"""

files['frontend/streamlit_app.py'] = """
import streamlit as st
from frontend.views import home, login, register, analyzer, results, history, profile
from frontend.services.auth_service import init_auth

st.set_page_config(
    page_title="Adhii ATS Resume",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_auth()

def main():
    st.sidebar.title("Adhii ATS Resume")
    
    if st.session_state.get('user'):
        st.sidebar.write(f"Logged in as {st.session_state.user.get('email', 'User')}")
        pages = {
            "Analyzer": analyzer.show,
            "History": history.show,
            "Profile": profile.show
        }
        selection = st.sidebar.radio("Navigation", list(pages.keys()))
        
        if st.sidebar.button("Logout"):
            from frontend.services.auth_service import logout
            logout()
            st.rerun()
            
        pages[selection]()
    else:
        pages = {
            "Home": home.show,
            "Login": login.show,
            "Register": register.show
        }
        selection = st.sidebar.radio("Navigation", list(pages.keys()))
        pages[selection]()

if __name__ == "__main__":
    main()
"""

files['frontend/assets/styles.css'] = """
/* Adhii ATS Resume Custom Styles */

:root {
    --primary-color: #4A90E2;
    --background-dark: #1E2129;
    --card-bg: #282C34;
    --text-primary: #E0E6ED;
    --text-secondary: #9DA5B4;
}

.stApp {
    background-color: var(--background-dark);
    color: var(--text-primary);
}

.stButton>button {
    background-color: var(--primary-color);
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #357ABD;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.css-1d391kg {
    background-color: var(--card-bg);
}

.card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255,255,255,0.05);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
}
"""

files['frontend/services/auth_service.py'] = """
import streamlit as st

def init_auth():
    if 'user' not in st.session_state:
        st.session_state['user'] = None

def login(email, password):
    # Placeholder
    st.session_state['user'] = {"email": email}
    return True

def logout():
    st.session_state['user'] = None
"""

files['frontend/views/home.py'] = """
import streamlit as st

def show():
    st.title("Adhii ATS Resume")
    st.markdown("### Make Your Resume Work for the Job You Want.")
    st.write("AI-powered resume-to-job matching")
"""

files['frontend/views/login.py'] = """
import streamlit as st
from frontend.services.auth_service import login

def show():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login(email, password):
            st.rerun()
"""

files['frontend/views/register.py'] = """
import streamlit as st

def show():
    st.title("Create Account")
    st.write("Registration flow placeholder")
"""

files['frontend/views/analyzer.py'] = """
import streamlit as st
from frontend.services.api_client import api_analyze_resume

def show():
    st.title("Resume Analyzer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Upload Resume")
        resume_file = st.file_uploader("Upload PDF, DOC, or DOCX", type=["pdf", "doc", "docx"])
        
    with col2:
        st.subheader("2. Job Description")
        job_title = st.text_input("Job Title (Optional)")
        company = st.text_input("Company (Optional)")
        job_desc = st.text_area("Paste Job Description", height=200)
        
    if st.button("ANALYZE RESUME", use_container_width=True):
        if not resume_file or not job_desc:
            st.error("Please provide both a resume and job description.")
            return
            
        with st.spinner("Analyzing resume..."):
            result = api_analyze_resume(resume_file, job_desc, job_title, company)
            st.session_state['analysis_result'] = result
            st.success("Analysis complete!")
            # Should ideally navigate to results, but for now we just show it.
            st.json(result)
"""

files['frontend/views/results.py'] = """
import streamlit as st

def show():
    st.title("Results Dashboard")
"""

files['frontend/views/history.py'] = """
import streamlit as st

def show():
    st.title("Analysis History")
"""

files['frontend/views/profile.py'] = """
import streamlit as st

def show():
    st.title("Profile")
"""

files['frontend/services/api_client.py'] = """
import requests
import streamlit as st

def get_backend_url():
    # In a real app we'd get this from st.secrets
    return "http://localhost:8000"

def api_analyze_resume(file, jd, title="", company=""):
    url = f"{get_backend_url()}/api/analyze"
    files = {"resume": (file.name, file.getvalue(), file.type)}
    data = {
        "job_description": jd,
        "job_title": title,
        "company_name": company
    }
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None
"""

for path, content in files.items():
    write_file(path, content)
    print(f"Created {path}")
