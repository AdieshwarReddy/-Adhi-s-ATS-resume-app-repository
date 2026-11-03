from fastapi import APIRouter
from backend.api import auth, analysis, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(analysis.router, tags=["Analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])

@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
