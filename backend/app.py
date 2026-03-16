from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List
import uvicorn
import os
import uuid
import asyncio
import base64
import aiohttp
import json
from datetime import datetime
from PIL import Image
import io

class ShoeImage(BaseModel):
    url: str
    file_type: str  # Coze 支持: 'image', 'video', 'audio', 'document', 'default'

class ProductReplacementRequest(BaseModel):
    shoe_images: List[ShoeImage]

class CreativeTemplateRequest(BaseModel):
    shoe_image: ShoeImage

app = FastAPI(
    title="FitGen API",
    description="虚拟试鞋系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
if not os.path.exists("files"):
    os.makedirs("files")
app.mount("/files", StaticFiles(directory="files"), name="files")

# 任务存储（内存存储，生产环境应使用数据库）
tasks = {}

# 模拟穿搭图数据
mock_poses = [
    {
        "id": "pose_1",
        "name": "模特穿搭1",
        "url": "/files/models/model1/pose1.jpg"
    },
    {
        "id": "pose_2",
        "name": "模特穿搭2",
        "url": "/files/models/model2/pose1.jpg"
    },
    {
        "id": "pose_3",
        "name": "模特穿搭3",
        "url": "/files/models/model3/pose1.jpg"
    }
]

# 确保目录存在
def ensure_directories():
    directories = [
        "files/models/model1",
        "files/models/model2", 
        "files/models/model3",
        "files/jobs",
        "files/shoes",
        "files/generated"
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

ensure_directories()

def save_and_compress_image(img_data, filename, max_width=1024, quality=85):
    """保存并压缩图片"""
    try:
        # 打开图片
        img = Image.open(io.BytesIO(img_data))
        
        # 如果图片太大，调整大小
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            try:
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            except AttributeError:
                img = img.resize((max_width, new_height), Image.LANCZOS)
        
        # 确保输出目录存在
        output_dir = "files/generated"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存图片
        output_path = os.path.join(output_dir, filename)
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        
        # 返回URL
        return f"/files/generated/{filename}"
    except Exception as e:
        print(f"图片处理失败: {e}")
        return None

@app.get("/api/poses")
async def get_poses():
    """获取穿搭图列表"""
    return mock_poses

@app.get("/api/product-images")
async def get_product_images():
    """获取商品展示图列表"""
    # 模拟数据
    return [
        {
            "id": "prod_1",
            "name": "商品展示1",
            "url": "/files/products/product1.jpg"
        },
        {
            "id": "prod_2",
            "name": "商品展示2", 
            "url": "/files/products/product2.jpg"
        }
    ]

@app.post("/api/jobs")
async def create_job(
    mode: str = Form(...),
    shoe_side: UploadFile = File(None),
    shoe_45: UploadFile = File(None),
    shoe_top: UploadFile = File(None),
    穿搭图_url: str = Form(None),
    pose_option: str = Form(None),
    clothes_option: str = Form(None),
    gen_type: str = Form(None),
    creative_style: str = Form(None)
):
    """创建任务"""
    # 生成任务ID
    job_id = str(uuid.uuid4())
    
    # 保存上传的图片
    uploaded_images = []
    if shoe_side:
        filename = f"shoe_side_{job_id}_{shoe_side.filename}"
        filepath = os.path.join("files", "shoes", filename)
        with open(filepath, "wb") as f:
            f.write(await shoe_side.read())
        uploaded_images.append("shoe_side")
    
    if shoe_45:
        filename = f"shoe_45_{job_id}_{shoe_45.filename}"
        filepath = os.path.join("files", "shoes", filename)
        with open(filepath, "wb") as f:
            f.write(await shoe_45.read())
        uploaded_images.append("shoe_45")
    
    if shoe_top:
        filename = f"shoe_top_{job_id}_{shoe_top.filename}"
        filepath = os.path.join("files", "shoes", filename)
        with open(filepath, "wb") as f:
            f.write(await shoe_top.read())
        uploaded_images.append("shoe_top")
    
    # 初始化任务状态
    tasks[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "mode": mode,
        "uploaded_images": uploaded_images,
        "params": {
            "穿搭图_url": 穿搭图_url,
            "pose_option": pose_option,
            "clothes_option": clothes_option,
            "gen_type": gen_type,
            "creative_style": creative_style
        },
        "results": []
    }
    
    # 异步处理任务
    async def process_job():
        await asyncio.sleep(3)  # 模拟处理时间
        tasks[job_id]["status"] = "processing"
        
        # 模拟生成结果
        await asyncio.sleep(5)  # 模拟生成时间
        
        # 根据模式生成不同的结果
        if mode == "fashion":
            # 生成3张穿搭图
            results = [
                f"/files/jobs/{job_id}_result_1.jpg",
                f"/files/jobs/{job_id}_result_2.jpg",
                f"/files/jobs/{job_id}_result_3.jpg"
            ]
        elif mode == "product":
            if gen_type == "3张商品展示图片":
                results = [
                    f"/files/jobs/{job_id}_product_1.jpg",
                    f"/files/jobs/{job_id}_product_2.jpg",
                    f"/files/jobs/{job_id}_product_3.jpg"
                ]
            else:
                # 视频结果
                results = [f"/files/jobs/{job_id}_video.mp4"]
        elif mode == "creative":
            # 生成多个创意模板
            results = [
                f"/files/jobs/{job_id}_creative_1.jpg",
                f"/files/jobs/{job_id}_creative_2.jpg",
                f"/files/jobs/{job_id}_creative_3.jpg"
            ]
        else:
            results = []
        
        tasks[job_id]["status"] = "done"
        tasks[job_id]["results"] = results
        tasks[job_id]["completed_at"] = datetime.now().isoformat()
    
    # 启动异步任务
    asyncio.create_task(process_job())
    
    return {
        "job_id": job_id,
        "status": "created",
        "message": f"任务创建成功，已上传 {len(uploaded_images)} 张图片"
    }

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    """获取任务状态"""
    if job_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return tasks[job_id]

# 商品展示替换
@app.post("/api/product-replacement")
async def product_replacement(
    request: ProductReplacementRequest
):
    """商品展示替换 - 使用流式调用"""
    try:
        # 调用Coze API - 使用stream_run接口
        url = "https://8j29cc8xjr.coze.site/stream_run"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUyMmYxMWE3LTM2Y2EtNGQ0Ny04NjEyLWVlZTk5MTg5MWM3YSJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIlM5bndJZU5NY1dkODByNlF5cURlSDlXbGQ2Rmk2YWsyIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzczNTIwMTU2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjE2NTYzMjY0ODg0ODM0MzUwIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjE3MjExMDY5OTI0MTE0NDk1In0.fisq-pz4GxkAhtSpeVQ2hj-o-Fhg_InvnxRD2RHNYFWW7bQFj32bPrDsJNEbyTzJwGI1Moyqd5xF9EIXNpDlHw1hfChjdZcktT7ADkvfLw2fVVx1k0EUhk0IdYuv8vxx0FBeux92jMp8thjHtTFFA0bsfJEUqbvgz_09puphf1qrxvneRxYQcveSyuWlMxEm--KALd9BtY8sJBdcFxWlH7YjGDX8GgNwaqp75mK_t_MWQnhJrX5MgYoFPZJl6RsQpmRHFR0d2bDIOD7Y1A77oCQEqVouDCemLLXekSgQGsfmyltZBM1juLrz41XqxzD8x2Si-a-0RGPNY9d67FmIWw",
            "Content-Type": "application/json",
        }
        
        # 将Pydantic模型转换为字典列表
        shoe_images_dict = [img.dict() for img in request.shoe_images]
        payload = {
            "shoe_images": shoe_images_dict
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                # 处理流式响应
                final_result = None
                async for line in response.content:
                    line_text = line.decode('utf-8').strip()
                    if line_text.startswith('data: '):
                        data = line_text[6:]
                        if data and data != '[DONE]':
                            try:
                                import json
                                result = json.loads(data)
                                final_result = result
                            except:
                                pass
                
                if final_result:
                    return {
                        "status": "success",
                        "result": final_result
                    }
                else:
                    return {
                        "status": "error",
                        "message": "未收到完整响应"
                    }
                
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 穿搭替换
class OutfitReplacementRequest(BaseModel):
    outfit_images: List[ShoeImage]
    shoe_images: List[ShoeImage]

@app.post("/api/outfit-replacement")
async def outfit_replacement(
    request: OutfitReplacementRequest
):
    """穿搭替换 - 使用简单返回"""
    try:
        # 调用Coze API - 使用stream_run接口
        url = "https://9rbhqjzw86.coze.site/stream_run"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUyMmYxMWE3LTM2Y2EtNGQ0Ny04NjEyLWVlZTk5MTg5MWM3YSJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkpRczZLdVVVUzU2TTI1eTdvQ0Q1dDduaDBLSVJySEg2Il0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzczNTI2ODg4LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjE2NTM3NTI3MzA1ODk1OTYyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjE3MjM5OTg1MjQ2MTc1MjU5In0.aycK7JEjHWnuxT1jNiGaszvDeWrWBNC0H5x1O3-Z9BIyCfxvKBrIycg_1A9z9owoDm9uQut2TPl9J4K-Vd3va3kkcWPReClhu3OuYJAiYWj8TSHkLQc3VrUvGfO3mqCXQjpa4eVd01Gfis-6kuPuYOxLAyNkCaw8iBRBCKnbzlZ3qxnUaa-HSMQApEClGo1OXy2XcZpKfkgjcrDy3RMdCB3xP8RbVhQzZmmhrgkzlyf5RfIg9oAfsL81Lum8AEeSXjeLZceDIKwBMdUgnHMGuwg2ncFJJWMUkGmwsHzbaGZJhYP-82EAv-HQbkaGe1gT0IEVOJGoNUlIGFnUq4G1WA",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        # 将Pydantic模型转换为字典列表
        outfit_images_dict = [img.dict() for img in request.outfit_images]
        shoe_images_dict = [img.dict() for img in request.shoe_images]
        payload = {
            "outfit_images": outfit_images_dict,
            "shoe_images": shoe_images_dict
        }

        final_result = None
        debug_info = []

        # 增加 timeout 到 180 秒
        timeout = aiohttp.ClientTimeout(total=180)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                debug_info.append(f"Coze API状态码: {response.status}")
                
                # 处理流式响应，收集所有数据
                line_count = 0
                async for line in response.content:
                    line_count += 1
                    line = line.decode('utf-8').strip()
                    
                    if line.startswith("data:"):
                        data_text = line[5:].strip()
                        if data_text and data_text != "[DONE]":
                            try:
                                parsed = json.loads(data_text)
                                final_result = parsed
                            except Exception as e:
                                pass
        
        # 如果有结果，下载图片并转成Base64（公网访问必须用Base64）
        if final_result and 'output' in final_result:
            output = final_result['output']
            if 'result_images' in output:
                result_images = output['result_images']
                for i, img_info in enumerate(result_images):
                    if 'url' in img_info:
                        try:
                            # 下载图片
                            async with aiohttp.ClientSession() as img_session:
                                async with img_session.get(img_info['url']) as img_resp:
                                    if img_resp.status == 200:
                                        img_data = await img_resp.read()
                                        # 转成Base64
                                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                                        # 替换URL为Base64
                                        img_info['url'] = f"data:image/jpeg;base64,{img_base64}"
                                        debug_info.append(f"✓ 图片{i+1}已转Base64")
                        except Exception as e:
                            debug_info.append(f"✗ 图片{i+1}转换失败: {str(e)}")
        
        debug_info.append(f"最终结果: {'有' if final_result else '无'}")
        
        if final_result:
            return final_result
        else:
            return {
                "status": "error", 
                "message": "未收到响应",
                "debug": debug_info
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API调用失败: {str(e)}")


@app.post("/api/creative-template")
async def creative_template(
    request: CreativeTemplateRequest
):
    """AI创意模板生成"""
    try:
        # 调用Coze API - 使用stream_run接口
        url = "https://8vy4zfg7xp.coze.site/stream_run"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjRkYTM5YTEyLTY3MjYtNDljZi05YzlmLTcyYWYzMjc4NDg1YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbInRrMWNoaHFmaFV5STZUSW01TTVZVWlYVDNDTm80alBhIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzczNTI5Nzg5LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjE3MTQxMzgxNzcyODY5Njk1Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjE3MjUyNDQ0OTc1NjYxMDk2In0.kyb-Typ2CM3Tw3ap-alF5ujD0WX3X6v8m6111CXrcftm5MUdbb_6G8p6LGBLXw2CtfwKEt2EdRgPqq2h4tZNAHClXll6y6HSgBn6hd9GI3usMITqqoGos8OBcSba5XSRZZDVtLwl1bXp9-FqHHTr_sP8T1JWxTdyCsXETpY4-XUWqgNv4emzWJ_uw23gEWAqHNZgpuALORhBinH4eM33say-r2jzZIg7cJMQIRfzE3ysiPvjs02NKM33vTLTyYwOUyRDYU-PoWgqNeRut_G33jaGZfOYhpAd1XSbnUG4933_pL_JOgTyL11qA_Alalv0HAZHkQIhKcFfW3Wyi9rFQQ",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        
        # 将Pydantic模型转换为字典
        payload = {
            "shoe_image": request.shoe_image.dict()
        }
        
        final_result = None
        debug_info = []

        # 增加 timeout 到 180 秒
        timeout = aiohttp.ClientTimeout(total=180)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                debug_info.append(f"Coze API状态码: {response.status}")
                
                # 处理流式响应，收集所有数据
                line_count = 0
                async for line in response.content:
                    line_count += 1
                    line = line.decode('utf-8').strip()
                    
                    if line.startswith("data:"):
                        data_text = line[5:].strip()
                        if data_text and data_text != "[DONE]":
                            try:
                                parsed = json.loads(data_text)
                                final_result = parsed
                            except Exception as e:
                                pass
        
        # 如果有结果，下载图片并转成Base64（公网访问必须用Base64）
        if final_result and 'output' in final_result:
            output = final_result['output']
            if 'doodle_images' in output:
                doodle_images = output['doodle_images']
                new_doodle_images = []
                for i, img_url in enumerate(doodle_images):
                    try:
                        # 下载图片
                        async with aiohttp.ClientSession() as img_session:
                            async with img_session.get(img_url) as img_resp:
                                if img_resp.status == 200:
                                    img_data = await img_resp.read()
                                    # 转成Base64
                                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                                    # 替换URL为Base64
                                    new_img_url = f"data:image/jpeg;base64,{img_base64}"
                                    new_doodle_images.append(new_img_url)
                                    debug_info.append(f"✓ 图片{i+1}已转Base64")
                                else:
                                    new_doodle_images.append(img_url)
                                    debug_info.append(f"✗ 图片{i+1}下载失败，使用原URL")
                    except Exception as e:
                        new_doodle_images.append(img_url)
                        debug_info.append(f"✗ 图片{i+1}转换失败: {str(e)}")
                # 替换doodle_images数组
                output['doodle_images'] = new_doodle_images
        
        debug_info.append(f"最终结果: {'有' if final_result else '无'}")
        
        if final_result:
            return final_result
        else:
            return {
                "status": "error", 
                "message": "未收到响应",
                "debug": debug_info
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API调用失败: {str(e)}")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "FitGen API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/poses": "获取穿搭图列表",
            "GET /api/product-images": "获取商品展示图列表",
            "POST /api/jobs": "创建任务",
            "GET /api/jobs/{job_id}": "获取任务状态"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
