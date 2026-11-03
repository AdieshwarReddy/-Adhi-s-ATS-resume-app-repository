from backend.models.schemas import CategoryScores
from typing import List

class RecommendationEngine:
    def generate_recommendations(self, missing_skills: List[str], scores: CategoryScores, sections: dict) -> List[str]:
        recommendations = []
        
        # High Priority
        if missing_skills:
            recommendations.append(f"[HIGH PRIORITY] Add evidence of missing required skills: {', '.join(missing_skills[:3])}.")
        if "experience" not in sections:
            recommendations.append("[HIGH PRIORITY] Clearly label your 'Experience' or 'Work History' section.")
            
        # Medium Priority
        if scores.content < 75:
            recommendations.append("[MEDIUM PRIORITY] Rewrite project or experience bullet points to include measurable impact (e.g., 'Improved efficiency by 20%').")
        if "summary" not in sections:
            recommendations.append("[MEDIUM PRIORITY] Add a professional summary aligned with the job description.")
            
        # Low Priority
        if scores.formatting < 90:
            recommendations.append("[LOW PRIORITY] Simplify resume formatting. Avoid complex tables or columns that might confuse ATS parsers.")
            
        if not recommendations:
            recommendations.append("Keep tailoring your resume for every specific job application.")
            
        return recommendations
        
    def generate_quick_actions(self, missing_skills: List[str]) -> List[str]:
        actions = []
        if missing_skills:
            actions.append(f"Incorporate '{missing_skills[0]}' into a recent project description if you have the experience.")
        actions.append("Quantify at least two bullet points in your most recent role.")
        actions.append("Ensure your contact information is at the very top and easily readable.")
        return actions
