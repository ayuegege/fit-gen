@echo off
cd /d d:\fit-gen\frontend
.venv\Scripts\streamlit.exe run app.py --server.address 0.0.0.0 --server.port 8501 --server.enableCORS false
pause
