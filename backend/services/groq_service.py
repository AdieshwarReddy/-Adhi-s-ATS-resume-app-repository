import os
from backend.core.config import settings

class GroqService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL or "qwen/qwen3.8-27b"
        self.fallback_models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
        try:
            from groq import Groq
            if self.api_key:
                self.client = Groq(api_key=self.api_key)
            else:
                self.client = None
        except ImportError:
            self.client = None

    def enhance_feedback(self, resume_text: str, jd_text: str, strengths: list, weaknesses: list) -> str:
        if not self.client:
            return self._fallback_feedback(weaknesses)
            
        prompt = f"""
        You are a premier executive ATS and career coach.
        Review this candidate's resume excerpt and the target job description.
        
        Job Description:
        {jd_text[:1200]}
        
        Resume Excerpt:
        {resume_text[:1200]}
        
        Identified Weaknesses / Missing Elements:
        {weaknesses}
        
        Provide high-impact, actionable guidance with these exact sections in clean markdown:
        
        ### 🎯 Executive Assessment & Role Fit
        A focused analysis of how the candidate matches the target role, identifying the critical gap they must close.
        
        ### 🚀 Top 3 High-Impact Improvements
        1. **Keyword Integration**: Where and how to integrate the missing technical keywords naturally into existing experience.
        2. **Quantified Impact**: How to rewrite passive duty bullets into measurable business achievements (Google X-Y-Z formula).
        3. **Section Optimization**: Specific adjustments to Professional Summary or Skills categorization to pass ATS filters.
        
        ### ✏️ Bullet Point Rewrite Example
        Provide an example showing a "Before (Weak/Generic)" bullet point transformed into an "After (High-Impact ATS-Optimized)" bullet point tailored to this job.
        
        Keep the response crisp, highly relevant, and professional.
        """
        
        models_to_try = [self.model] + [m for m in self.fallback_models if m != self.model]
        
        for candidate_model in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an elite ATS optimization expert and career strategist."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=candidate_model,
                    temperature=0.4,
                    max_tokens=650
                )
                content = response.choices[0].message.content.strip()
                if content:
                    return content
            except Exception:
                continue

        return self._fallback_feedback(weaknesses)

    def _fallback_feedback(self, weaknesses: list) -> str:
        weakness_bullets = "\n".join([f"- **Focus on**: {w}" for w in weaknesses[:4]]) if weaknesses else "- Align experience with target keywords."
        return f"""
### 🎯 Executive Assessment & Role Fit
Your resume exhibits strong foundational qualifications but requires targeted keyword density and metric-driven evidence to reach the 85+ ATS interview threshold for this role.

### 🚀 Top 3 High-Impact Improvements
1. **Keyword Integration**:
{weakness_bullets}
2. **Quantified Impact**: Transform passive responsibility statements into metric-backed accomplishments (e.g., latency reduction, cost savings, user scale).
3. **ATS Formatting**: Ensure all skill names match the exact casing and phrasing used in the job description to maximize automated parser recognition.

### ✏️ Bullet Point Rewrite Example
- **Before**: "Responsible for maintaining and updating backend services and database queries."
- **After**: "Architected and optimized 8+ RESTful microservices, reducing query latency by 35% and improving API throughput across 50k+ daily active users."
"""
