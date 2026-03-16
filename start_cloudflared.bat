@echo off
cd /d d:\fit-gen
echo ========================================
echo   Start Cloudflare Tunnel
echo ========================================
echo.
echo Waiting for URL...
echo.
cloudflared tunnel --url http://localhost:8501
pause
