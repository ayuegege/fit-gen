@echo off
cd /d d:\fit-gen\backend
.venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 120
pause
