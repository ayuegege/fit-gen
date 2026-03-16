#!/usr/bin/env python3
"""
FitGen 启动器 - 同时启动后端和前端
"""
import subprocess
import sys
import os
import time
import webbrowser
import threading

def start_backend():
    """启动后端服务"""
    backend_dir = os.path.join(os.path.dirname(sys.executable), 'backend')
    if not os.path.exists(backend_dir):
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    cmd = [sys.executable, '-m', 'uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8000']
    subprocess.Popen(cmd, cwd=backend_dir)
    print("✓ 后端服务已启动: http://localhost:8000")

def start_frontend():
    """启动前端服务"""
    frontend_dir = os.path.join(os.path.dirname(sys.executable), 'frontend')
    if not os.path.exists(frontend_dir):
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
           '--server.port', '8501', '--server.address', '0.0.0.0',
           '--server.headless', 'true', '--server.enableCORS', 'false']
    subprocess.Popen(cmd, cwd=frontend_dir)
    print("✓ 前端服务已启动: http://localhost:8501")

def open_browser():
    """等待服务启动后打开浏览器"""
    time.sleep(5)
    webbrowser.open('http://localhost:8501')
    print("✓ 已打开浏览器")

def main():
    print("=" * 60)
    print("  黑潮AI定制系统 - FitGen")
    print("=" * 60)
    print()
    
    # 启动后端
    start_backend()
    
    # 等待后端启动
    time.sleep(2)
    
    # 启动前端
    start_frontend()
    
    # 在后台打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print()
    print("系统已启动！")
    print("- 前端页面: http://localhost:8501")
    print("- 后端API: http://localhost:8000")
    print()
    print("按 Ctrl+C 停止服务")
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        sys.exit(0)

if __name__ == '__main__':
    main()
