@echo off
echo Starting Adhii ATS Resume Backend and Frontend...
start "Adhii ATS - FastAPI Backend" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul
start "Adhii ATS - Streamlit Frontend" cmd /k "python -m streamlit run frontend/streamlit_app.py --server.port 8501"
echo.
echo ========================================================
echo  Adhii ATS Resume is running:
echo  - Frontend UI:  http://localhost:8501
echo  - Backend API:  http://localhost:8000
echo  - API Docs:     http://localhost:8000/docs
echo ========================================================
pause

