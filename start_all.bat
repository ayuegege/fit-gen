@echo off
echo ========================================
echo   Black Tide AI - Start All Services
echo ========================================
echo.

echo [1/3] Starting backend service (port 8000)...
start "Backend Service" cmd /k "cd /d d:\fit-gen\backend && .venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 120"

echo [2/3] Starting frontend service (port 8501)...
start "Frontend Service" cmd /k "cd /d d:\fit-gen\frontend && .venv\Scripts\streamlit.exe run app.py --server.address 0.0.0.0 --server.port 8501 --server.enableCORS false"

echo [3/3] Waiting for services to start...
timeout /t 8 /nobreak >nul

echo.
echo Starting Cloudflare Tunnel...
echo.
echo Please wait for the URL to appear below...
echo.

:: 启动 cloudflared
cloudflared tunnel --url http://localhost:8501

pause
