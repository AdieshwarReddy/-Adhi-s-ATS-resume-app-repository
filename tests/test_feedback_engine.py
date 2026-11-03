from backend.services.feedback_engine import FeedbackEngine
from backend.models.schemas import CategoryScores, ResumeData, JobDescriptionData

def test_feedback_generation():
    engine = FeedbackEngine()
    resume = ResumeData(filename="r.txt", text="a", sections={"experience": "a", "summary": "a"})
    jd = JobDescriptionData(title="a", company="a", text="a")
    scores = CategoryScores(formatting=95, keywords=80, content=80, skill_validation=90, ats_compatibility=80)
    
    feedback = engine.generate_feedback(resume, jd, scores, ["Python"], [])
    
    assert "strengths" in feedback
    assert "weaknesses" in feedback
    assert any("Strong alignment" in s for s in feedback["strengths"])
    assert any("No major weaknesses" in w for w in feedback["weaknesses"])
