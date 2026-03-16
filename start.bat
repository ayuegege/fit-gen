@echo off
chcp 65001 >nul
echo ========================================
echo   黑潮AI定制系统 - FitGen
echo ========================================
echo.
echo 正在启动服务...
echo.

cd /d "%~dp0backend"
start /B python -m uvicorn app:app --host 0.0.0.0 --port 8000
echo ✓ 后端服务启动: http://localhost:8000
echo.

cd /d "%~dp0frontend"
start /B python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
echo ✓ 前端服务启动: http://localhost:8501
echo.

timeout /t 3 >nul
start http://localhost:8501
echo ✓ 已打开浏览器
echo.
echo ========================================
echo   服务运行中，不要关闭此窗口
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

pause
