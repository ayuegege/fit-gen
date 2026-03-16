# FitGen Windows 打包说明

## 方法一：使用 GitHub Actions 自动打包（推荐）

### 步骤：

1. **在 GitHub 创建仓库**
   - 访问 https://github.com/new
   - 创建名为 `fit-gen` 的仓库
   - 设置为 Private（私密）

2. **上传代码**
   ```bash
   # 在 fit-gen-new 目录下
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/fit-gen.git
   git push -u origin main
   ```

3. **配置 GitHub Actions**
   - 创建 `.github/workflows/build.yml` 文件
   - 我已帮你写好配置，见下方

4. **推送到 GitHub**
   - 代码推送后，GitHub 会自动打包
   - 在 Actions 页面查看进度
   - 完成后在 Releases 下载 exe

---

## 方法二：本地 Windows 打包

### 环境准备：

1. **安装 Python 3.10+**
   - 下载：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **下载项目代码**
   - 把整个 `fit-gen-new` 文件夹复制到 Windows 电脑

3. **运行打包脚本**
   ```cmd
   cd fit-gen-new
   build_windows.bat
   ```

4. **获取 exe**
   - 打包完成后，exe 在 `dist\FitGen.exe`

---

## GitHub Actions 配置文件

创建文件：`.github/workflows/build.yml`

```yaml
name: Build Windows EXE

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pyinstaller
        pip install fastapi uvicorn streamlit aiohttp pillow requests pydantic starlette
    
    - name: Build EXE
      run: pyinstaller FitGen_Windows.spec --clean
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: FitGen-Windows
        path: dist/FitGen.exe
    
    - name: Create Release
      if: github.event_name == 'push' && github.ref == 'refs/heads/main'
      uses: softprops/action-gh-release@v1
      with:
        files: dist/FitGen.exe
        tag_name: v${{ github.run_number }}
        name: FitGen Windows Build ${{ github.run_number }}
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 使用方法

### 发给别人的使用步骤：

1. **发送文件**
   - 把 `FitGen.exe` 发给对方
   - 文件大小约 150-200MB

2. **运行程序**
   - 双击 `FitGen.exe`
   - 等待几秒，会自动打开浏览器
   - 浏览器访问 http://localhost:8501

3. **使用系统**
   - 选择"穿搭替换"模式
   - 上传穿搭图（3张）
   - 上传鞋子图（3张）
   - 点击生成

---

## 注意事项

- Windows 可能需要允许防火墙访问
- 第一次运行可能需要等待几秒
- 确保 8000 和 8501 端口未被占用
- 关闭程序：按 Ctrl+C 或直接关闭窗口
