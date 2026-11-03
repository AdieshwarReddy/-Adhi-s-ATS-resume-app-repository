from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from starlette.concurrency import run_in_threadpool
from typing import Optional
from backend.services.resume_analyzer import ResumeAnalyzerService
from backend.services.resume_parser import ResumeParser

router = APIRouter()
analyzer_service = ResumeAnalyzerService()
parser = ResumeParser()

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(""),
    job_description_file: Optional[UploadFile] = File(None),
    job_title: str = Form(""),
    company_name: str = Form("")
):
    if not resume.filename:
        raise HTTPException(status_code=400, detail="No resume file uploaded")
        
    ext = resume.filename.split('.')[-1].lower() if '.' in resume.filename else ""
    if ext not in ["pdf", "doc", "docx"]:
        raise HTTPException(status_code=400, detail="Unsupported resume file extension. Only PDF, DOC, DOCX are allowed.")
        
    final_jd_text = (job_description or "").strip()
    
    # If job description file is uploaded, extract text from it
    if job_description_file and job_description_file.filename:
        jd_ext = job_description_file.filename.split('.')[-1].lower() if '.' in job_description_file.filename else ""
        if jd_ext not in ["pdf", "doc", "docx", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported job description file extension. Allowed: PDF, DOC, DOCX, TXT.")
        try:
            jd_bytes = await job_description_file.read()
            if len(jd_bytes) > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Job description file too large. Maximum size is 10MB.")
            parsed_jd = await run_in_threadpool(parser.parse_file, jd_bytes, job_description_file.filename, job_description_file.content_type)
            extracted_jd_text = parsed_jd.get("text", "").strip()
            if extracted_jd_text:
                if final_jd_text:
                    final_jd_text = final_jd_text + "\n\n" + extracted_jd_text
                else:
                    final_jd_text = extracted_jd_text
        except HTTPException:
            raise
        except Exception as e:
            if not final_jd_text:
                raise HTTPException(status_code=400, detail=f"Failed to read job description file: {str(e)}")

    if not final_jd_text:
        raise HTTPException(status_code=400, detail="Please provide a job description by pasting text or uploading a PDF/DOCX file.")

    try:
        file_bytes = await resume.read()
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Resume file too large. Maximum size is 10MB.")
            
        result = await run_in_threadpool(
            analyzer_service.analyze,
            file_bytes=file_bytes,
            filename=resume.filename,
            content_type=resume.content_type,
            jd_text=final_jd_text,
            title=job_title,
            company=company_name
        )
            
        result_dict = result.model_dump()
        return result_dict
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
