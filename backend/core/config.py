import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen/qwen3.8-27b"
    
    FRONTEND_URL: str = "http://localhost:8501"
    BACKEND_URL: str = "http://localhost:8000"
    
    SENTENCE_TRANSFORMER_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    SPACY_MODEL: str = "en_core_web_md"
    
    MAX_UPLOAD_MB: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
