from backend.models.schemas import AnalysisResult, ResumeData, JobDescriptionData
from backend.services.resume_parser import ResumeParser
from backend.services.jd_matcher import JDAnalyzer
from backend.services.semantic_matcher import SemanticMatcher
from backend.services.ats_scorer import ATSScorer
from backend.services.feedback_engine import FeedbackEngine
from backend.services.recommendation_engine import RecommendationEngine
from backend.services.groq_service import GroqService

class ResumeAnalyzerService:
    def __init__(self):
        self.parser = ResumeParser()
        self.jd_analyzer = JDAnalyzer()
        self.semantic_matcher = SemanticMatcher()
        self.scorer = ATSScorer()
        self.feedback = FeedbackEngine()
        self.recommendations = RecommendationEngine()
        self.groq = GroqService()

    def analyze(self, file_bytes: bytes, filename: str, content_type: str, jd_text: str, title: str = "", company: str = "") -> AnalysisResult:
        # 1. Parse Resume
        parsed = self.parser.parse_file(file_bytes, filename, content_type)
        resume_data = ResumeData(
            filename=parsed["filename"],
            text=parsed["text"],
            sections=parsed["sections"]
        )
        
        # 2. Extract JD Data
        jd_data = self.jd_analyzer.analyze(jd_text, title, company)
        
        # 3. Extract Resume Skills
        from backend.services.skill_extractor import SkillExtractor
        skill_extractor = SkillExtractor()
        resume_skills = skill_extractor.extract_skills(resume_data.text)
        resume_data.skills = resume_skills
        
        # 4. Compare Skills
        req_skills_set = set([s.lower() for s in jd_data.required_skills])
        res_skills_set = set([s.lower() for s in resume_skills])
        
        matched_skills = list(req_skills_set.intersection(res_skills_set))
        missing_skills = list(req_skills_set.difference(res_skills_set))
        
        # 5. Semantic Match
        semantic_sim = self.semantic_matcher.calculate_similarity(resume_data.text, jd_data.text)
        
        # 6. ATS Score
        overall_score, category_scores = self.scorer.score(resume_data, jd_data, semantic_sim, matched_skills, missing_skills)
        
        # 7. Feedback & Recommendations
        feedback_data = self.feedback.generate_feedback(resume_data, jd_data, category_scores, matched_skills, missing_skills)
        recs = self.recommendations.generate_recommendations(missing_skills, category_scores, resume_data.sections)
        actions = self.recommendations.generate_quick_actions(missing_skills)
        
        # 8. AI Enhancements (Groq)
        ai_suggestion = self.groq.enhance_feedback(resume_data.text, jd_data.text, feedback_data["strengths"], feedback_data["weaknesses"])
        
        return AnalysisResult(
            overall_score=overall_score,
            semantic_similarity=semantic_sim,
            scores=category_scores,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            matched_keywords=[], # We can extract matched keywords similarly
            missing_keywords=[],
            strengths=feedback_data["strengths"],
            weaknesses=feedback_data["weaknesses"],
            recommendations=recs,
            quick_actions=actions,
            ai_suggestions=ai_suggestion
        )
