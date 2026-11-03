import os
from jinja2 import Environment, FileSystemLoader
from backend.models.schemas import AnalysisResult
from backend.core.config import settings

class ReportGenerator:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        os.makedirs(self.template_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # Create a basic template if none exists
        template_path = os.path.join(self.template_dir, 'report.html')
        if not os.path.exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Adhii ATS Resume Report</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; color: #333; }
                        h1 { color: #4A90E2; }
                        .score-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
                        .highlight { font-weight: bold; color: #4A90E2; }
                        .footer { margin-top: 40px; font-size: 0.8em; color: #777; border-top: 1px solid #ddd; padding-top: 10px; }
                    </style>
                </head>
                <body>
                    <h1>Adhii ATS Resume Analysis</h1>
                    
                    <div class="score-card">
                        <h2>Overall Score: <span class="highlight">{{ result.overall_score }}/100</span></h2>
                        <p>Semantic Similarity: {{ "%.2f"|format(result.semantic_similarity * 100) }}%</p>
                    </div>
                    
                    <div class="score-card">
                        <h3>Score Breakdown</h3>
                        <ul>
                            <li>Formatting: {{ result.scores.formatting }}</li>
                            <li>Keywords: {{ result.scores.keywords }}</li>
                            <li>Content: {{ result.scores.content }}</li>
                            <li>Skill Validation: {{ result.scores.skill_validation }}</li>
                            <li>ATS Compatibility: {{ result.scores.ats_compatibility }}</li>
                        </ul>
                    </div>
                    
                    <div class="score-card">
                        <h3>Matched Skills</h3>
                        <p>{{ result.matched_skills | join(', ') if result.matched_skills else 'None' }}</p>
                    </div>
                    
                    <div class="score-card">
                        <h3>Missing Skills</h3>
                        <p>{{ result.missing_skills | join(', ') if result.missing_skills else 'None' }}</p>
                    </div>
                    
                    <div class="score-card">
                        <h3>Recommendations</h3>
                        <ul>
                        {% for rec in result.recommendations %}
                            <li>{{ rec }}</li>
                        {% endfor %}
                        </ul>
                    </div>
                    
                    <div class="footer">
                        Disclaimer: Scores are estimates based on resume/job-description analysis and do not represent results from any specific employer's proprietary ATS.
                    </div>
                </body>
                </html>
                """)

    def generate_html(self, result: AnalysisResult) -> bytes:
        try:
            template = self.env.get_template('report.html')
            
            # Use model_dump for Pydantic v2
            html_out = template.render(result=result.model_dump() if hasattr(result, "model_dump") else result.dict())
            
            return html_out.encode('utf-8')
        except Exception as e:
            return f"HTML Generation Failed: {e}".encode('utf-8')
