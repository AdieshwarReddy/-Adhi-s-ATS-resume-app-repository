import io
import re
from typing import Dict, Any

try:
    import pymupdf
    import fitz  # pymupdf alias
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None

class ResumeParser:
    def __init__(self):
        pass

    def parse_file(self, file_bytes: bytes, filename: str, content_type: str) -> Dict[str, Any]:
        text = ""
        ext = filename.split('.')[-1].lower() if '.' in filename else ""
        
        if ext == 'pdf' or content_type == 'application/pdf':
            text = self._parse_pdf(file_bytes)
        elif ext in ['docx', 'doc'] or 'word' in content_type:
            text = self._parse_docx(file_bytes)
        else:
            # Fallback to plain text if possible
            try:
                text = file_bytes.decode('utf-8')
            except:
                raise ValueError("Unsupported file format or encoding")
                
        text = self._clean_text(text)
        sections = self._extract_sections(text)
        
        return {
            "filename": filename,
            "text": text,
            "sections": sections
        }

    def _parse_pdf(self, file_bytes: bytes) -> str:
        if not fitz:
            # fallback or mock
            return "PDF Parsing not available without pymupdf"
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            return text
        except Exception as e:
            return f"Error parsing PDF: {e}"

    def _parse_docx(self, file_bytes: bytes) -> str:
        if not docx:
            return "DOCX Parsing not available without python-docx"
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"Error parsing DOCX: {e}"

    def _clean_text(self, text: str) -> str:
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_sections(self, text: str) -> Dict[str, str]:
        # Very basic regex-based section extraction
        # Real ATS use complex NLP for this, we will approximate
        sections = {}
        
        keywords = {
            "experience": r"(?i)\b(experience|employment|work history)\b",
            "education": r"(?i)\b(education|academic|qualifications)\b",
            "skills": r"(?i)\b(skills|technologies|tools)\b",
            "summary": r"(?i)\b(summary|profile|objective)\b",
            "projects": r"(?i)\b(projects)\b"
        }
        
        # Simple extraction: find keywords and slice text
        # This is a naive implementation; a real one would be more robust
        positions = []
        for key, pattern in keywords.items():
            match = re.search(pattern, text)
            if match:
                positions.append((match.start(), key))
                
        positions.sort()
        
        if not positions:
            sections["unclassified"] = text
            return sections
            
        # extract text between keywords
        for i in range(len(positions)):
            start_pos, key = positions[i]
            if i < len(positions) - 1:
                end_pos = positions[i+1][0]
                content = text[start_pos:end_pos]
            else:
                content = text[start_pos:]
            sections[key] = content.strip()
            
        return sections
