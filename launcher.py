#!/usr/bin/env python3
"""
FitGen 启动器 - 调用系统 Python 启动服务
不打包依赖，只作为启动器使用
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
    
    # 获取项目目录
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境路径
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    backend_dir = os.path.join(app_dir, 'backend')
    frontend_dir = os.path.join(app_dir, 'frontend')
    
    print(f"项目目录: {app_dir}")
    print()
    
    # 检查 Python 是否可用
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True, timeout=5)
        print(f"Python 版本: {result.stdout.strip()}")
    except:
        print("错误: 找不到 Python！")
        print("请先安装 Python 3.11+")
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 启动后端
    print("\n启动后端服务...")
    backend_cmd = ['python', '-m', 'uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8000']
    backend_proc = subprocess.Popen(backend_cmd, cwd=backend_dir, 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("✓ 后端服务已启动: http://localhost:8000")
    
    # 启动前端
    print("\n启动前端服务...")
    frontend_cmd = ['python', '-m', 'streamlit', 'run', 'app.py', 
                     '--server.port', '8501', '--server.address', '0.0.0.0',
                     '--server.headless', 'true']
    frontend_proc = subprocess.Popen(frontend_cmd, cwd=frontend_dir,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("✓ 前端服务已启动: http://localhost:8501")
    
    # 等待启动完成
    print("\n等待服务启动...")
    time.sleep(5)
    
    # 打开浏览器
    print("打开浏览器...")
    webbrowser.open('http://localhost:8501')
    print("✓ 浏览器已打开")
    
    print("\n" + "=" * 60)
    print("  系统已启动！")
    print("  前端: http://localhost:8501")
    print("  后端: http://localhost:8000")
    print("=" * 60)
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        # 等待进程结束
        while True:
            time.sleep(1)
            # 检查进程是否还在运行
            if backend_proc.poll() is not None:
                print("\n后端服务已停止")
                break
            if frontend_proc.poll() is not None:
                print("\n前端服务已停止")
                break
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("✓ 服务已停止")
    
    print("\n按回车键退出...")
    input()

if __name__ == '__main__':
    main()
