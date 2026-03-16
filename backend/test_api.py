import json
import base64
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")

async def test_api():
    print("测试API请求格式...")
    
    # 构建测试数据
    shoe_image = "test"  # 这里用假数据测试格式
    pose_image = "test"  # 这里用假数据测试格式
    
    # 构建正确的API请求格式
    payload = {
        "model": "qwen-image-2.0",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image": f"data:image/jpeg;base64,{shoe_image}"  # 鞋图
                        },
                        {
                            "type": "image",
                            "image": f"data:image/jpeg;base64,{pose_image}"  # 模特图
                        },
                        {
                            "type": "text",
                            "text": "请把第一张图中的鞋子自然地合成到第二张图中模特的脚上，保持光影真实、透视准确，生成一张逼真的试鞋效果图"
                        }
                    ]
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    
    print("请求体格式:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    
    # 检查必要的字段
    required_fields = ["model", "input", "input.messages"]
    
    for field in required_fields:
        if field == "model":
            if "model" not in payload:
                print(f"❌ 缺少字段: {field}")
            else:
                print(f"✅ 字段存在: {field}")
        elif field == "input.messages":
            if "input" not in payload or "messages" not in payload["input"]:
                print(f"❌ 缺少字段: {field}")
            else:
                print(f"✅ 字段存在: {field}")
    
    print("\n测试完成，请求格式正确！")

if __name__ == "__main__":
    asyncio.run(test_api())