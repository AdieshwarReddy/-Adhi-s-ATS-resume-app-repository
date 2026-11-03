from backend.services.semantic_matcher import SemanticMatcher

def test_semantic_matching():
    matcher = SemanticMatcher()
    score = matcher.calculate_similarity("Software Engineer with Python", "Looking for Python Software Developer")
    assert 0.0 <= score <= 1.0
