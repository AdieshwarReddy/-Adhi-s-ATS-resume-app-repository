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
