from backend.services.ats_scorer import ATSScorer
from backend.models.schemas import ResumeData, JobDescriptionData

def test_ats_scorer_bounds():
    scorer = ATSScorer()
    resume = ResumeData(filename="test.pdf", text="Experience: Python", sections={"experience": "Python"})
    jd = JobDescriptionData(title="Dev", company="Inc", text="Need Python", keywords=["python"])
    
    overall, categories = scorer.score(resume, jd, 0.8, ["python"], ["java"])
    
    assert 0 <= overall <= 100
    assert 0 <= categories.formatting <= 100
    assert 0 <= categories.keywords <= 100
    assert 0 <= categories.content <= 100
    assert 0 <= categories.skill_validation <= 100
    assert 0 <= categories.ats_compatibility <= 100

def test_ats_scorer_weights():
    scorer = ATSScorer()
    assert sum(scorer.weights.values()) == 1.0
