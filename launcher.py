#!/usr/bin/env python3
"""
FitGen 启动器 - 同时启动后端和前端（修复版）
"""
import subprocess
import sys
import os
import time
import webbrowser
import psutil

def is_process_running(process_name):
    """检查进程是否已运行"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def start_backend():
    """启动后端服务"""
    backend_dir = os.path.join(os.path.dirname(sys.executable), 'backend')
    if not os.path.exists(backend_dir):
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # 检查是否已启动
    if is_process_running('uvicorn'):
        print("✓ 后端服务已在运行")
        return
    
    cmd = [sys.executable, '-m', 'uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8000']
    subprocess.Popen(cmd, cwd=backend_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ 后端服务已启动: http://localhost:8000")

def start_frontend():
    """启动前端服务"""
    frontend_dir = os.path.join(os.path.dirname(sys.executable), 'frontend')
    if not os.path.exists(frontend_dir):
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # 检查是否已启动
    if is_process_running('streamlit'):
        print("✓ 前端服务已在运行")
        return
    
    cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
           '--server.port', '8501', '--server.address', '0.0.0.0',
           '--server.headless', 'true', '--server.enableCORS', 'false']
    subprocess.Popen(cmd, cwd=frontend_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ 前端服务已启动: http://localhost:8501")

def open_browser_once():
    """打开浏览器（只打开一次）"""
    time.sleep(3)
    webbrowser.open('http://localhost:8501')
    print("✓ 已打开浏览器")

def main():
    print("=" * 60)
    print("  黑潮AI定制系统 - FitGen")
    print("=" * 60)
    print()
    
    # 启动服务
    start_backend()
    time.sleep(2)
    start_frontend()
    
    # 打开浏览器
    open_browser_once()
    
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
        # 清理进程
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] in ['uvicorn', 'streamlit']:
                    proc.terminate()
        except:
            pass
        sys.exit(0)

if __name__ == '__main__':
    main()
