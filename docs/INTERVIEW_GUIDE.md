# Interview Guide: Adhii ATS Resume

Use these answers to explain the core engineering decisions during placement interviews.

### 1. What problem does the project solve?
It bridges the gap between how a candidate writes a resume and how an automated Applicant Tracking System (ATS) reads it. It prevents highly qualified candidates from being rejected simply due to keyword mismatches or poor formatting, providing actionable insights to fix those issues.

### 2. Why FastAPI?
FastAPI was chosen for its high performance, native async support (ideal for handling I/O bound operations like file uploads and external API calls), and automatic OpenAPI documentation. Pydantic validation ensures the payload shapes are strict and secure.

### 3. Why Streamlit?
Streamlit allows rapid development of data-centric web applications. It abstracts away complex React/frontend state management, letting me focus on the AI/ML integration and data visualization while still looking professional with custom CSS.

### 4. Why Supabase?
Supabase offers an open-source alternative to Firebase built on standard PostgreSQL. It provides robust authentication, immediate REST/GraphQL APIs, and most importantly, Row Level Security (RLS) directly at the database layer.

### 5. How authentication works
Authentication uses Supabase's email/password auth. When a user logs in, they receive a JWT. The frontend stores this in session state. 

### 6. Why service role keys cannot enter the frontend
The `SUPABASE_SERVICE_ROLE_KEY` bypasses all Row Level Security. If exposed in the Streamlit client, anyone could inspect the network or source and gain full read/write access to every user's private resumes. The frontend strictly uses the `SUPABASE_ANON_KEY`.

### 7. Resume parsing flow
Resumes (PDF, DOCX) are uploaded as binary streams. The backend uses `pymupdf` for PDF text extraction and `python-docx` for Word documents. A regex-based heuristics engine then segments the raw text into distinct sections (e.g., Experience, Education).

### 8. How spaCy is used
`en_core_web_md` is used for Named Entity Recognition (NER) to find non-standard tech tools that might not exist in a hardcoded taxonomy, and for tokenizing complex sentences during skill extraction.

### 9. What Sentence Transformers are
They are neural networks fine-tuned to map sentences and paragraphs into a dense vector space (embeddings). They capture the contextual meaning of text, not just exact words.

### 10. What all-MiniLM-L6-v2 does
It's a specific, lightweight Sentence Transformer model. It is extremely fast while maintaining high accuracy, making it perfect for real-time inference in a web request lifecycle without requiring a massive GPU.

### 11. What embeddings are
Embeddings are arrays of floating-point numbers representing the semantic meaning of text. Words with similar meanings will have vectors that point in similar directions.

### 12. What cosine similarity means
It is a mathematical measure of similarity between two non-zero vectors. It measures the angle between them; a score of 1 means identical direction (meaning), 0 means orthogonal (unrelated).

### 13. Why semantic similarity is better than keyword matching alone
A candidate might write "Led frontend engineering using React", while the JD asks for "Senior UI Developer with JavaScript framework experience." Keyword matching fails here. Semantic similarity understands these concepts are highly related.

### 14. ATS scoring formula
A weighted combination of factors: Formatting (10%), Keywords (25%), Content semantic match (30%), Skill validation (25%), and ATS compatibility checks (10%). This prevents "keyword stuffing" from achieving a 100% score.

### 15. Keyword matching
It uses regex with word boundaries `\b` and a taxonomy dictionary to normalize aliases (e.g., `scikit-learn` vs `sklearn`), ensuring fair evaluation regardless of how a candidate spells a tool.

### 16. Skill validation
It distinguishes between a skill merely listed in a comma-separated list versus one supported by context in the "Experience" section, rewarding candidates who provide evidence of their skills.

### 17. Feedback engine
A deterministic rules engine that generates immediate Strengths and Weaknesses based on the numerical outputs of the scoring engine (e.g., if skill score < 50%, output "Missing critical skills").

### 18. Recommendation engine
Categorizes actionable advice into High, Medium, and Low priorities based on the severity of the score deficit, telling the user exactly what to fix first.

### 19. Role of Groq
Groq (using LLMs like LLaMA 3) acts as a career coach. It reads the deterministic weaknesses and the actual resume text to generate a highly specific, natural-language paragraph of advice (e.g., "Rewrite your third bullet point under Company X to include metrics...").

### 20. Why Groq is not responsible for the numerical score
LLMs are non-deterministic and prone to hallucinations. They might give a resume an 80 one day and a 60 the next. The core numerical score must be consistent, explainable, and reproducible using the deterministic engine.

### 21. PDF generation architecture
`Jinja2` injects the JSON analysis results into a structured HTML template. `WeasyPrint` then renders this HTML and associated CSS into a downloadable, print-friendly PDF binary stream.

### 22. Supabase database design
Uses a relational model: A `profiles` table linked to `auth.users`, and a `resume_analyses` table holding the JSON structured results and scores. We avoid storing raw parsed text to minimize PII exposure risks.

### 23. Row Level Security (RLS)
PostgreSQL policies enforce that a user's JWT `auth.uid()` must match the `user_id` column on the table. This guarantees a user can only `SELECT`, `INSERT`, or `DELETE` their own data, natively protecting against IDOR vulnerabilities.

### 24. Security
- Input validation via Pydantic
- File size limits (10MB max)
- MIME type and extension whitelists
- No local persistent storage of uploads (processed in memory/temp)
- Secrets managed entirely via `.env` and Render/Streamlit secret managers.

### 25. Deployment
The backend runs on Render, which natively supports Python and allows installing system-level dependencies for WeasyPrint. The frontend is hosted on Streamlit Community Cloud.

### 26. Biggest engineering challenges
1. Reconciling deterministic scoring with NLP: Balancing strict keyword logic with fuzzy semantic matching.
2. Managing the heavy ML models: Ensuring Sentence Transformers only load into memory once at startup via the Singleton pattern rather than on every request.
3. Cross-platform WeasyPrint dependencies.

### 27. Limitations
The system approximates generic ATS logic but does not perfectly replicate proprietary systems like Workday or Taleo, which often have their own closed-source parsing quirks.

### 28. How I would improve the project at scale
- Move the ML inference and PDF generation to asynchronous Celery workers to prevent HTTP timeout on large resumes.
- Implement a vector database (like pgvector in Supabase) to allow users to search their past resumes for specific skills.
- Add caching for standard job descriptions (e.g., standard "Software Engineer" JD embeddings).
