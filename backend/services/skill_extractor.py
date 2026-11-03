import re
from typing import List

# Simple skill taxonomy dictionary for deterministic fallback
SKILL_TAXONOMY = {
    "python": ["python", "python3"],
    "java": ["java", "core java"],
    "cpp": ["c++", "cpp", "c/c++"],
    "javascript": ["javascript", "js", "es6"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node", "node.js", "nodejs"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "supabase": ["supabase"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["cv", "computer vision"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "docker": ["docker", "containerization"],
    "git": ["git", "github", "gitlab"],
    "ci/cd": ["ci/cd", "ci-cd", "continuous integration"]
}

class SkillExtractor:
    _nlp = None
    _nlp_attempted = False

    def __init__(self):
        if not SkillExtractor._nlp_attempted:
            SkillExtractor._nlp_attempted = True
            try:
                import spacy
                from backend.core.config import settings
                try:
                    SkillExtractor._nlp = spacy.load(settings.SPACY_MODEL)
                except (OSError, Exception):
                    SkillExtractor._nlp = None
            except (ImportError, Exception):
                SkillExtractor._nlp = None
        self.nlp = SkillExtractor._nlp

    def extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        extracted = set()
        
        # 1. Deterministic extraction based on taxonomy
        for canonical, aliases in SKILL_TAXONOMY.items():
            for alias in aliases:
                # Use word boundaries to match exactly
                pattern = r'\b' + re.escape(alias) + r'\b'
                if re.search(pattern, text_lower):
                    extracted.add(canonical)
                    break # if one alias matches, add canonical and move to next canonical
        
        # 2. NLP-based extraction (fallback/enhancement)
        if self.nlp:
            doc = self.nlp(text)
            # Find Proper Nouns which might be tools/technologies not in taxonomy
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT'] and len(ent.text) > 1:
                    # we could add more filtering here, but we will keep it simple
                    pass
            
        return list(extracted)
