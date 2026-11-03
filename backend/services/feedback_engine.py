from backend.models.schemas import ResumeData, JobDescriptionData, CategoryScores
from typing import List, Dict

class FeedbackEngine:
    def generate_feedback(self, resume: ResumeData, jd: JobDescriptionData, scores: CategoryScores, matched: List[str], missing: List[str]) -> Dict[str, List[str]]:
        strengths = []
        weaknesses = []
        
        # Strengths
        if scores.skill_validation > 80:
            strengths.append("Strong alignment with required job skills.")
        if len(matched) > 5:
            strengths.append(f"Demonstrates solid foundation in core technologies like {', '.join(matched[:3])}.")
        if scores.formatting > 80:
            strengths.append("Resume structure is clean and ATS-friendly.")
        if "experience" in resume.sections:
            strengths.append("Experience section is clearly identifiable.")
            
        # Weaknesses
        if scores.skill_validation < 50:
            weaknesses.append("Missing several critical skills mentioned in the job description.")
        if len(missing) > 0:
            weaknesses.append(f"Lacks explicit mention of: {', '.join(missing[:3])}.")
        if "summary" not in resume.sections:
            weaknesses.append("Missing a professional summary or objective.")
        if scores.ats_compatibility < 70:
            weaknesses.append("Potential issues parsing text; formatting might be too complex or lacking standard headers.")
            
        if not strengths:
            strengths.append("Resume contains valid text format.")
            
        if not weaknesses:
            weaknesses.append("No major weaknesses detected, but continue to tailor to the specific role.")
            
        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }
