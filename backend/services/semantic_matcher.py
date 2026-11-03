from backend.core.config import settings

class SemanticMatcher:
    _model = None
    _initialized = False

    def __init__(self):
        if not SemanticMatcher._initialized:
            SemanticMatcher._initialized = True
            try:
                from sentence_transformers import SentenceTransformer
                SemanticMatcher._model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
            except (ImportError, Exception):
                SemanticMatcher._model = None
        self.model = SemanticMatcher._model

    def calculate_similarity(self, text1: str, text2: str) -> float:
        if not self.model:
            # Deterministic word overlap similarity fallback when neural model is offline
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 or not words2:
                return 0.5
            overlap = len(words1.intersection(words2)) / max(1, len(words2))
            return min(0.95, max(0.40, round(0.40 + (overlap * 0.55), 2)))
            
        try:
            from sentence_transformers import util
            embeddings1 = self.model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.model.encode(text2, convert_to_tensor=True)
            
            cosine_scores = util.cos_sim(embeddings1, embeddings2)
            # return as float between 0 and 1
            return float(cosine_scores[0][0])
        except Exception:
            return 0.70
