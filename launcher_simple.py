#!/usr/bin/env python3
"""
FitGen 简化版启动器 - 只启动前端
"""
import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("=" * 60)
    print("  黑潮AI定制系统 - FitGen")
    print("=" * 60)
    print()
    
    # 获取目录
    frontend_dir = os.path.join(os.path.dirname(sys.executable), 'frontend')
    if not os.path.exists(frontend_dir):
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # 启动前端（streamlit）
    cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', 
           '--server.port', '8501', '--server.address', '0.0.0.0',
           '--server.headless', 'true']
    
    print("正在启动服务...")
    proc = subprocess.Popen(cmd, cwd=frontend_dir)
    
    # 等待启动后打开浏览器
    time.sleep(5)
    webbrowser.open('http://localhost:8501')
    
    print("✓ 服务已启动: http://localhost:8501")
    print()
    print("按 Ctrl+C 停止服务")
    print()
    
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        proc.terminate()

if __name__ == '__main__':
    main()
