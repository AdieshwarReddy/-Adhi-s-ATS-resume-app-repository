from backend.models.schemas import CategoryScores, ResumeData, JobDescriptionData
import re

class ATSScorer:
    def __init__(self):
        # Configurable weights
        self.weights = {
            "formatting": 0.10,
            "keywords": 0.25,
            "content": 0.30,
            "skill_validation": 0.25,
            "ats_compatibility": 0.10
        }

    def score(self, resume: ResumeData, jd: JobDescriptionData, semantic_sim: float, matched_skills: list, missing_skills: list) -> tuple[int, CategoryScores]:
        formatting = self._score_formatting(resume)
        keywords = self._score_keywords(resume.text, jd.keywords)
        content = self._score_content(semantic_sim, resume.sections)
        skill_validation = self._score_skills(matched_skills, missing_skills)
        ats_comp = self._score_ats_compatibility(resume)
        
        overall = int(
            (formatting * self.weights["formatting"]) +
            (keywords * self.weights["keywords"]) +
            (content * self.weights["content"]) +
            (skill_validation * self.weights["skill_validation"]) +
            (ats_comp * self.weights["ats_compatibility"])
        )
        
        scores = CategoryScores(
            formatting=formatting,
            keywords=keywords,
            content=content,
            skill_validation=skill_validation,
            ats_compatibility=ats_comp
        )
        
        return max(0, min(100, overall)), scores

    def _score_formatting(self, resume: ResumeData) -> int:
        score = 50
        if len(resume.sections) >= 3:
            score += 25
        if len(resume.text) > 100:
            score += 25
        return min(100, score)
        
    def _score_keywords(self, text: str, keywords: list) -> int:
        if not keywords:
            return 80
        matched = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()))
        ratio = matched / len(keywords)
        return int(ratio * 100)
        
    def _score_content(self, semantic_sim: float, sections: dict) -> int:
        # Base score on semantic similarity (0.0 to 1.0)
        base = int(semantic_sim * 80)
        if "experience" in sections:
            base += 10
        if "projects" in sections:
            base += 10
        return min(100, base)
        
    def _score_skills(self, matched: list, missing: list) -> int:
        total = len(matched) + len(missing)
        if total == 0:
            return 80
        return int((len(matched) / total) * 100)
        
    def _score_ats_compatibility(self, resume: ResumeData) -> int:
        score = 80 # Base assumption if parsed
        if not resume.text.strip():
            return 0
        if "contact" in resume.sections or "email" in resume.text.lower():
            score += 20
        return min(100, score)
