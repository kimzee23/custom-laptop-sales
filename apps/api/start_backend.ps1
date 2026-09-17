# REALTECH Custom Laptop Store - FastAPI Backend Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " REALTECH CUSTOM LAPTOP STORE - FASTAPI BACKEND" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Starting FastAPI Backend on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host " Swagger API Documentation: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host " ReDoc API Documentation:   http://127.0.0.1:8000/redoc" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
