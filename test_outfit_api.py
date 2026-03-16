#!/usr/bin/env python3
"""
测试穿搭替换 API
"""
import requests
import json
import time

# API 端点
url = "http://localhost:8000/api/outfit-replacement"

# 测试数据 - 使用公网可访问的图片 URL
# Coze 工作流要求上传 3 张穿搭图和 3 张鞋子图
test_data = {
    "outfit_images": [
        {
            "url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800",
            "file_type": "image"
        },
        {
            "url": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800",
            "file_type": "image"
        },
        {
            "url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800",
            "file_type": "image"
        }
    ],
    "shoe_images": [
        {
            "url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
            "file_type": "image"
        },
        {
            "url": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=800",
            "file_type": "image"
        },
        {
            "url": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=800",
            "file_type": "image"
        }
    ]
}

print("=" * 60)
print("测试穿搭替换 API")
print("=" * 60)
print(f"请求 URL: {url}")
print(f"请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
print()

# 发送请求
print("发送请求...")
start_time = time.time()

try:
    response = requests.post(url, json=test_data, timeout=120)

    elapsed_time = time.time() - start_time
    print(f"响应时间: {elapsed_time:.2f} 秒")
    print(f"状态码: {response.status_code}")
    print()

    if response.status_code == 200:
        result = response.json()
        print("响应结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("错误响应:")
        print(response.text)

except requests.exceptions.Timeout:
    elapsed_time = time.time() - start_time
    print(f"请求超时（等待 {elapsed_time:.2f} 秒）")

except Exception as e:
    elapsed_time = time.time() - start_time
    print(f"请求失败（等待 {elapsed_time:.2f} 秒）: {str(e)}")

print()
print("=" * 60)
