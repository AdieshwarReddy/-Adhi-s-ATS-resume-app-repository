# Architecture of Adhii ATS Resume

The system is a monolithic full-stack web application designed for processing documents (resumes) and applying NLP and ML models in near real-time.

```mermaid
graph TD
    User([User]) -->|Interacts with| Streamlit[Streamlit Frontend]
    Streamlit -->|API Requests| FastAPI[FastAPI Backend]
    
    subgraph "Backend Services"
        FastAPI -->|Parse| Parser[Resume Parser]
        Parser -.-> PyMuPDF
        Parser -.-> python-docx
        
        FastAPI -->|Extract Skills| SkillExt[Skill Extractor]
        SkillExt -.-> spaCy
        
        FastAPI -->|Match JD| JDMatch[JD Analyzer]
        
        FastAPI -->|Compare Meaning| SemMatch[Semantic Matcher]
        SemMatch -.-> SentTransformers[Sentence-Transformers]
        
        FastAPI -->|Score| Scorer[ATS Scorer]
        
        FastAPI -->|Enhance| Groq[Groq Service]
        Groq -.-> LLM API
        
        FastAPI -->|Generate Report| Weasy[WeasyPrint PDF Generator]
    end
    
    FastAPI <-->|Auth & History| Supabase[(Supabase PostgreSQL)]
```

## Data Flow
1. **Upload & Input**: User provides a PDF/DOCX resume and pastes a Job Description in the Streamlit UI.
2. **Transfer**: Streamlit sends a `multipart/form-data` request to FastAPI (`/api/analyze`).
3. **Parsing**: The `ResumeParser` extracts raw text and identifies structural sections (e.g., Experience, Skills).
4. **Analysis Pipeline**:
   - `SkillExtractor` extracts technical skills via a deterministic taxonomy and spaCy NER.
   - `JDAnalyzer` extracts requirements from the job description.
   - `SemanticMatcher` uses `all-MiniLM-L6-v2` to calculate cosine similarity between the resume text and the job description.
   - `ATSScorer` aggregates the formatting, keyword matches, and semantic similarity into a final score (0-100).
5. **Feedback Generation**: `FeedbackEngine` and `RecommendationEngine` build deterministic actionable points. `GroqService` enhances this with contextual AI advice if configured.
6. **Persistence**: Analysis results are saved to Supabase against the user's UUID.
7. **Delivery**: The structured JSON response is rendered by Streamlit into interactive charts and cards.
8. **Export**: The user can request a PDF report, generating an HTML template via Jinja2 which WeasyPrint converts to a PDF blob.
