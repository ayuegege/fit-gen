#!/usr/bin/env python3
"""
直接测试 Coze API
"""
import requests
import json
import time

# Coze 工作流 URL
url = "https://9rbhqjzw86.coze.site/stream_run"

# Coze API Key
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUyMmYxMWE3LTM2Y2EtNGQ0Ny04NjEyLWVlZTk5MTg5MWM3YSJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkpRczZLdVVVUzU2TTI1eTdvQ0Q1dDduaDBLSVJySEg2Il0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzczNTI2ODg4LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjE2NTM3NTI3MzA1ODk1OTYyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjE3MjM5OTg1MjQ2MTc1MjU5In0.aycK7JEjHWnuxT1jNiGaszvDeWrWBNC0H5x1O3-Z9BIyCfxvKBrIycg_1A9z9owoDm9uQut2TPl9J4K-Vd3va3kkcWPReClhu3OuYJAiYWj8TSHkLQc3VrUvGfO3mqCXQjpa4eVd01Gfis-6kuPuYOxLAyNkCaw8iBRBCKnbzlZ3qxnUaa-HSMQApEClGo1OXy2XcZpKfkgjcrDy3RMdCB3xP8RbVhQzZmmhrgkzlyf5RfIg9oAfsL81Lum8AEeSXjeLZceDIKwBMdUgnHMGuwg2ncFJJWMUkGmwsHzbaGZJhYP-82EAv-HQbkaGe1gT0IEVOJGoNUlIGFnUq4G1WA",
    "Content-Type": "application/json",
}

# 请求参数
payload = {
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
print("直接测试 Coze API")
print("=" * 60)
print()

# 使用流式请求
print("发送流式请求...")
start_time = time.time()

try:
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=180)

    elapsed_time = time.time() - start_time
    print(f"连接建立时间: {elapsed_time:.2f} 秒")
    print(f"状态码: {response.status_code}")
    print()

    line_count = 0
    final_result = None

    print("接收流式响应...")
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8').strip()
            line_count += 1

            if line.startswith("data:"):
                data_text = line[5:].strip()

                if data_text == "[DONE]":
                    print(f"[Line {line_count}] 完成")
                    break
                else:
                    try:
                        parsed = json.loads(data_text)
                        final_result = parsed

                        # 打印重要事件
                        if 'type' in parsed:
                            event_type = parsed.get('type')
                            print(f"[Line {line_count}] 事件类型: {event_type}")

                        # 如果是成功结果，打印摘要
                        if parsed.get('type') == 'success' or 'output' in parsed:
                            print(f"[Line {line_count}] 收到结果!")
                            if 'output' in parsed:
                                output = parsed['output']
                                if 'result_images' in output:
                                    print(f"  - 生成图片数: {len(output['result_images'])}")
                    except json.JSONDecodeError as e:
                        print(f"[Line {line_count}] JSON 解析失败: {data_text[:100]}")

    total_time = time.time() - start_time
    print()
    print(f"总耗时: {total_time:.2f} 秒")
    print(f"总行数: {line_count}")

    if final_result:
        print()
        print("最终结果:")
        print(json.dumps(final_result, indent=2, ensure_ascii=False)[:500])
    else:
        print()
        print("未收到最终结果")

except requests.exceptions.Timeout:
    total_time = time.time() - start_time
    print(f"请求超时（等待 {total_time:.2f} 秒）")

except Exception as e:
    total_time = time.time() - start_time
    print(f"请求失败（等待 {total_time:.2f} 秒）: {str(e)}")

print()
print("=" * 60)
