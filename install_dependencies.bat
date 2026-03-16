@echo off
chcp 65001 >nul
echo ========================================
echo   安装依赖
echo ========================================
echo.
echo 正在检查 Python 版本...
python --version
if errorlevel 1 (
    echo.
    echo [错误] 未检测到 Python！
    echo 请先安装 Python 3.11+ 并添加到环境变量
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo 正在安装依赖...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败！
    echo.
) else (
    echo.
    echo [成功] 依赖安装完成！
    echo.
)

echo 按任意键退出...
pause >nul
