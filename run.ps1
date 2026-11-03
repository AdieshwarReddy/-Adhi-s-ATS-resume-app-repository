Write-Host "Starting Adhii ATS Resume Backend and Frontend..." -ForegroundColor Cyan

Start-Process wt -ArgumentList 'new-tab --title "FastAPI Backend" powershell -NoExit -Command "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"' -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) {
    Start-Process powershell -ArgumentList '-NoExit', '-Command', 'python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000'
}

Start-Sleep -Seconds 3

Start-Process wt -ArgumentList 'new-tab --title "Streamlit Frontend" powershell -NoExit -Command "python -m streamlit run frontend/streamlit_app.py --server.port 8501"' -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) {
    Start-Process powershell -ArgumentList '-NoExit', '-Command', 'python -m streamlit run frontend/streamlit_app.py --server.port 8501'
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " Adhii ATS Resume is running:" -ForegroundColor Green
Write-Host " - Frontend UI:  http://localhost:8501" -ForegroundColor Yellow
Write-Host " - Backend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host " - API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Green

