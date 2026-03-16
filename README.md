# 黑潮AI定制系统 - FitGen

虚拟试鞋系统 - 上传鞋子图片和穿搭图，一键替换鞋子

## 项目结构

```
fit-gen-new/
├── backend/          # FastAPI 后端
│   ├── app.py        # 主程序
│   └── files/        # 静态文件
├── frontend/         # Streamlit 前端
│   └── app.py        # 主程序
├── launcher.py       # 启动器
├── build_windows.bat # Windows 打包脚本
├── FitGen_Windows.spec # PyInstaller 配置
└── .github/workflows/ # GitHub Actions 配置
```

## 使用方式

### 方式一：飞书对话（最简单）
- 直接发 3 张穿搭图 + 3 张鞋子图给我
- 我帮你生成替换结果

### 方式二：前端页面
- 访问 http://localhost:8501
- 上传图片，点击生成

### 方式三：后端 API
```bash
curl -X POST http://localhost:8000/api/outfit-replacement \
  -H "Content-Type: application/json" \
  -d '{
    "outfit_images": [{"url": "...", "file_type": "image"}],
    "shoe_images": [{"url": "...", "file_type": "image"}]
  }'
```

## 打包 Windows EXE

### 方法一：GitHub Actions（推荐）
1. 把代码推送到 GitHub
2. GitHub 自动打包 Windows exe
3. 在 Releases 下载

### 方法二：本地 Windows 打包
1. 安装 Python 3.10+
2. 运行 `build_windows.bat`
3. 获取 `dist/FitGen.exe`

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| GET /api/poses | 获取穿搭图列表 |
| POST /api/outfit-replacement | 穿搭替换 |
| POST /api/product-replacement | 商品展示 |
| POST /api/creative-template | AI创意模板 |

## 配置

编辑 `backend/.env`：
```
BAILIAN_API_KEY=your_api_key
WORKFLOW_ID=your_workflow_id
```

## 依赖

```
fastapi
uvicorn
streamlit
aiohttp
pillow
requests
pydantic
```

## 启动

```bash
# 同时启动前后端
python launcher.py

# 或分别启动
# 后端
cd backend && python -m uvicorn app:app --port 8000

# 前端
cd frontend && streamlit run app.py --server.port 8501
```
