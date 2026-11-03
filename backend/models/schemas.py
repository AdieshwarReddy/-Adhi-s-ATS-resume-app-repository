from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class CategoryScores(BaseModel):
    formatting: int
    keywords: int
    content: int
    skill_validation: int
    ats_compatibility: int

class AnalysisResult(BaseModel):
    overall_score: int
    semantic_similarity: float
    scores: CategoryScores
    matched_skills: List[str]
    missing_skills: List[str]
    matched_keywords: List[str]
    missing_keywords: List[str]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    quick_actions: List[str]
    ai_suggestions: Optional[str] = None

class JobDescriptionData(BaseModel):
    title: str
    company: str
    text: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    keywords: List[str] = []

class ResumeData(BaseModel):
    filename: str
    text: str
    sections: Dict[str, str] = {}
    skills: List[str] = []
