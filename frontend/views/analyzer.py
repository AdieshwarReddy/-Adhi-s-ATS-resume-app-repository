import streamlit as st
import io
from frontend.services.api_client import api_analyze_resume

def extract_text_from_file(file_obj) -> str:
    if not file_obj:
        return ""
    try:
        file_bytes = file_obj.getvalue()
        fname = file_obj.name.lower()
        if fname.endswith(".pdf"):
            import fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
            return text.strip()
        elif fname.endswith((".docx", ".doc")):
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()]).strip()
        else:
            return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return ""

def show():
    st.markdown("<h1 style='text-align: center;'>Resume Intelligence Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--text-secondary); margin-bottom: 2rem;'>Upload your resume and target job description to get an in-depth ATS evaluation, graph analytics, and AI coaching.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📄 1. Upload Resume")
        st.info("Supported formats: PDF, DOCX (Max 10MB)")
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "doc", "docx"], label_visibility="collapsed")
        if resume_file:
            st.success(f"✓ {resume_file.name} uploaded successfully")
        
    with col2:
        st.markdown("### 💼 2. Target Job")
        job_title = st.text_input("Job Title (Optional)", placeholder="e.g. Senior Software Engineer")
        company = st.text_input("Company (Optional)", placeholder="e.g. Tech Corp")
        
        st.markdown("**Job Description Input:**")
        jd_mode = st.radio(
            "JD Input Method",
            ["📄 Upload JD File (PDF / DOCX)", "✍️ Paste Text Directly"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        final_jd_text = ""
        jd_file = None
        
        if "Upload" in jd_mode:
            st.caption("Upload the job description document as a PDF, DOCX, or TXT file:")
            jd_file = st.file_uploader("Upload Job Description PDF", type=["pdf", "doc", "docx", "txt"], key="jd_file_uploader", label_visibility="collapsed")
            if jd_file:
                st.success(f"✓ {jd_file.name} uploaded")
                extracted = extract_text_from_file(jd_file)
                if extracted:
                    st.caption(f"📝 Extracted content from **{jd_file.name}** ({len(extracted.split())} words) — you can review or adjust below:")
                    final_jd_text = st.text_area("Extracted JD Text", value=extracted, height=170, label_visibility="collapsed")
                else:
                    final_jd_text = st.text_area("Job Description", height=170, placeholder="Paste job description if PDF text could not be extracted...", label_visibility="collapsed")
        else:
            final_jd_text = st.text_area("Job Description", height=200, placeholder="Paste the full job description here...", label_visibility="collapsed")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_empty1, col_btn, col_empty2 = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 ANALYZE COMPATIBILITY", use_container_width=True):
            if not resume_file:
                st.error("⚠️ Please upload your resume to proceed.")
                return
            if not final_jd_text.strip() and not jd_file:
                st.error("⚠️ Please provide a job description by uploading a PDF/DOCX or pasting the text.")
                return
                
            with st.status("🧠 Analyzing your profile against the job description...", expanded=True) as status:
                st.write("Extracting resume structure and skills...")
                st.write("Parsing target job requirements from document...")
                st.write("Computing semantic match with sentence embeddings...")
                st.write("Evaluating ATS compatibility and scoring...")
                st.write("Generating AI career coach suggestions...")
                
                result = api_analyze_resume(
                    file=resume_file,
                    jd=final_jd_text,
                    jd_file=jd_file,
                    title=job_title,
                    company=company
                )
                
                if result:
                    st.session_state['analysis_result'] = result
                    st.session_state.pop('generated_report_bytes', None)
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    st.rerun()
                else:
                    status.update(label="❌ Analysis Failed", state="error", expanded=False)
