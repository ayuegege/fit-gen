#!/usr/bin/env python3
"""
测试穿搭替换并返回图片给飞书
"""
import requests
import json
import time
import base64
import os

# 后端 API
url = "http://localhost:8000/api/outfit-replacement"

# 测试数据
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
print()

# 发送请求
print("发送请求...（预计需要 2-3 分钟）")
start_time = time.time()

try:
    response = requests.post(url, json=test_data, timeout=200)

    elapsed_time = time.time() - start_time
    print(f"响应时间: {elapsed_time:.2f} 秒")
    print(f"状态码: {response.status_code}")
    print()

    if response.status_code == 200:
        result = response.json()
        print("响应结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 提取图片
        if result.get('type') == 'workflow_end' and 'output' in result:
            output = result['output']
            if 'result_images' in output:
                result_images = output['result_images']
                print(f"\n生成图片数: {len(result_images)}")

                # 保存图片到文件
                output_dir = "/workspace/projects/workspace/fit-gen-new/test_output"
                os.makedirs(output_dir, exist_ok=True)

                saved_files = []
                for i, img_info in enumerate(result_images):
                    if 'url' in img_info:
                        img_url = img_info['url']

                        # 如果是 Base64 图片
                        if img_url.startswith('data:image'):
                            # 提取 Base64 数据
                            header, data = img_url.split(',', 1)
                            img_data = base64.b64decode(data)

                            # 保存文件
                            filename = f"outfit_result_{i+1}.jpg"
                            filepath = os.path.join(output_dir, filename)
                            with open(filepath, 'wb') as f:
                                f.write(img_data)
                            saved_files.append(filepath)
                            print(f"✓ 保存图片: {filepath}")
                        else:
                            print(f"✗ 图片 {i+1} 不是 Base64 格式: {img_url[:100]}")

                print(f"\n总共保存 {len(saved_files)} 张图片")
                print(f"保存目录: {output_dir}")
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
