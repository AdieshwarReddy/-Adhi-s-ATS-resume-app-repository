from backend.services.skill_extractor import SkillExtractor

def test_skill_aliases_normalize_correctly():
    extractor = SkillExtractor()
    skills = extractor.extract_skills("I have experience in Scikit-Learn and python3")
    assert "scikit-learn" in skills
    assert "python" in skills
