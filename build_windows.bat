@echo off
chcp 65001
setlocal EnableDelayedExpansion

echo ===========================================
echo   黑潮AI定制系统 - FitGen
echo   Windows 打包工具
echo ===========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 检查 Python 环境... OK

REM 安装依赖
echo [2/5] 安装打包依赖...
pip install pyinstaller fastapi uvicorn streamlit aiohttp pillow requests pydantic starlette -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [3/5] 安装依赖... OK

REM 打包
echo [4/5] 正在打包（这可能需要几分钟）...
pyinstaller FitGen_Windows.spec --clean
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [5/5] 打包完成！
echo.
echo 打包结果保存在: dist\FitGen.exe
echo.
echo 使用方法:
echo   1. 把 dist\FitGen.exe 发给对方
echo   2. 双击运行即可
echo.
pause
