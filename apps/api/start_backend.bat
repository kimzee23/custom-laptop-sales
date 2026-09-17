@echo off
echo ===================================================
echo REALTECH CUSTOM LAPTOP STORE - FASTAPI BACKEND
echo ===================================================
echo Starting FastAPI Backend Server on http://127.0.0.1:8000
echo Swagger API Documentation: http://127.0.0.1:8000/docs
echo ReDoc API Documentation:   http://127.0.0.1:8000/redoc
echo ===================================================

cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py -3.13 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
) else (
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
)

pause
