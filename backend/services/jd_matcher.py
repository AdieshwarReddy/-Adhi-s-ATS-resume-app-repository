from backend.models.schemas import JobDescriptionData
from backend.services.skill_extractor import SkillExtractor

class JDAnalyzer:
    def __init__(self):
        self.skill_extractor = SkillExtractor()

    def analyze(self, jd_text: str, title: str = "", company: str = "") -> JobDescriptionData:
        # Extract skills from JD
        skills = self.skill_extractor.extract_skills(jd_text)
        
        # Determine basic required/preferred splits if possible (mocked for now)
        required = skills[:max(1, len(skills) * 3 // 4)]
        preferred = skills[max(1, len(skills) * 3 // 4):]
        
        # Simple keywords extraction (just splitting by spaces and keeping long words, mock implementation)
        import re
        words = re.findall(r'\b\w{5,}\b', jd_text.lower())
        from collections import Counter
        keywords = [word for word, count in Counter(words).most_common(15) if word not in skills]
        
        return JobDescriptionData(
            title=title,
            company=company,
            text=jd_text,
            required_skills=required,
            preferred_skills=preferred,
            keywords=keywords[:10]
        )
