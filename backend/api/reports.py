from fastapi import APIRouter, Response, HTTPException
from starlette.concurrency import run_in_threadpool
from backend.services.report_generator import ReportGenerator
from backend.models.schemas import AnalysisResult

router = APIRouter()
report_generator = ReportGenerator()

@router.post("/generate")
async def generate_report(result: AnalysisResult):
    try:
        html_bytes = await run_in_threadpool(report_generator.generate_html, result)
        
        if isinstance(html_bytes, bytes) and not html_bytes.startswith(b"HTML Generation Failed"):
            return Response(content=html_bytes, media_type="text/html", headers={
                "Content-Disposition": "attachment; filename=analysis_report.html"
            })
        else:
            raise HTTPException(status_code=500, detail="Failed to generate HTML")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
