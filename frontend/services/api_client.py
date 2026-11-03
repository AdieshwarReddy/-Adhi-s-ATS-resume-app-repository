import requests
import streamlit as st
import os

def get_backend_url():
    url = None
    try:
        url = st.secrets.get("BACKEND_URL")
    except Exception:
        pass
    if not url:
        url = os.getenv("BACKEND_URL", "http://localhost:8000")
    return url

def _analyze_in_process(file, jd="", jd_file=None, title="", company=""):
    """In-process execution fallback for Streamlit Community Cloud and standalone mode."""
    try:
        from backend.services.resume_analyzer import ResumeAnalyzerService
        from backend.services.resume_parser import ResumeParser
        
        parser = ResumeParser()
        analyzer = ResumeAnalyzerService()
        
        final_jd = (jd or "").strip()
        if jd_file is not None and hasattr(jd_file, "getvalue"):
            jd_bytes = jd_file.getvalue()
            parsed_jd = parser.parse_file(jd_bytes, jd_file.name, getattr(jd_file, "type", "application/pdf"))
            extracted_jd = parsed_jd.get("text", "").strip()
            if extracted_jd:
                final_jd = f"{final_jd}\n\n{extracted_jd}".strip() if final_jd else extracted_jd

        if not final_jd:
            raise ValueError("Please provide a job description by pasting text or uploading a file.")

        result = analyzer.analyze(
            file_bytes=file.getvalue(),
            filename=file.name,
            content_type=getattr(file, "type", "application/pdf"),
            jd_text=final_jd,
            title=title or "",
            company=company or ""
        )
        return result.model_dump() if hasattr(result, "model_dump") else result.dict()
    except Exception as e:
        st.error(f"Analysis engine error: {str(e)}")
        return None

def api_analyze_resume(file, jd="", jd_file=None, title="", company=""):
    url = f"{get_backend_url()}/api/analyze"
    files = {"resume": (file.name, file.getvalue(), file.type)}
    if jd_file is not None:
        files["job_description_file"] = (jd_file.name, jd_file.getvalue(), getattr(jd_file, 'type', 'application/pdf'))
    data = {
        "job_description": jd or "",
        "job_title": title or "",
        "company_name": company or ""
    }
    headers = {}
    if st.session_state.get('access_token'):
        headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
        
    try:
        # Connect to FastAPI backend with a short timeout
        response = requests.post(url, files=files, data=data, headers=headers, timeout=12)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Graceful fallback: If FastAPI server is not running or app is deployed standalone on Streamlit Cloud
        return _analyze_in_process(file, jd=jd, jd_file=jd_file, title=title, company=company)
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            st.error(e.response.text)
        return None

def api_get_history():
    url = f"{get_backend_url()}/api/analyses/"
    headers = {}
    if st.session_state.get('access_token'):
        headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
    try:
        response = requests.get(url, headers=headers, timeout=4)
        response.raise_for_status()
        return response.json()
    except:
        return []

def api_download_report(analysis_result_dict):
    url = f"{get_backend_url()}/api/reports/generate"
    try:
        response = requests.post(url, json=analysis_result_dict, timeout=8)
        response.raise_for_status()
        return response.content
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # In-process report generation fallback
        try:
            from backend.services.report_generator import ReportGenerator
            from backend.models.schemas import AnalysisResult
            generator = ReportGenerator()
            res_obj = AnalysisResult(**analysis_result_dict) if isinstance(analysis_result_dict, dict) else analysis_result_dict
            return generator.generate_html(res_obj)
        except Exception as e:
            st.error(f"Failed to generate HTML report: {e}")
            return None
    except Exception as e:
        st.error(f"Failed to generate HTML report: {e}")
        return None
