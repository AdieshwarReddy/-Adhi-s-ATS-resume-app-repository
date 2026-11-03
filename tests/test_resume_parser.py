import pytest
from backend.services.resume_parser import ResumeParser
import io

def test_resume_parser_fallback():
    parser = ResumeParser()
    text = "John Doe\nExperience: 5 years\nSkills: Python, Java"
    result = parser.parse_file(text.encode('utf-8'), "test.txt", "text/plain")
    assert result["filename"] == "test.txt"
    assert "John Doe" in result["text"]
    assert "experience" in result["sections"]
    assert "skills" in result["sections"]

def test_empty_file():
    parser = ResumeParser()
    result = parser.parse_file(b"", "empty.txt", "text/plain")
    assert result["text"] == ""

def test_invalid_file():
    parser = ResumeParser()
    with pytest.raises(ValueError):
        # random bytes that can't be decoded as utf-8 and not pdf/docx
        parser.parse_file(b"\xff\xfe\x00", "invalid.xyz", "application/octet-stream")
