import requests
from bs4 import BeautifulSoup
import os
import time
import random
from urllib.parse import urljoin

class IHuiwaImageCrawler:
    def __init__(self, save_path='./ihuiwa_images'):
        self.save_path = save_path
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.ihuiwa.com/'
        }
        
        # 创建保存目录
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"📁 创建目录：{save_path}")
    
    def get_all_images(self, url):
        """
        爬取指定页面的所有图片
        """
        try:
            # 发送请求
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"❌ 请求失败，状态码：{response.status_code}")
                return []
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有图片标签
            img_tags = soup.find_all('img')
            print(f"🔍 找到 {len(img_tags)} 张图片")
            
            # 提取图片URL
            img_urls = []
            for img in img_tags:
                img_url = img.get('src') or img.get('data-src') or img.get('data-original')
                if img_url:
                    # 处理相对URL
                    full_url = urljoin(url, img_url)
                    img_urls.append(full_url)
            
            # 去重
            unique_urls = list(set(img_urls))
            print(f"✅ 去重后剩余 {len(unique_urls)} 张图片")
            
            return unique_urls
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return []
    
    def download_image(self, img_url, save_path):
        """
        下载单张图片
        """
        try:
            # 随机延迟，避免被封
            time.sleep(random.uniform(0.5, 1.5))
            
            # 发送请求
            response = requests.get(img_url, headers=self.headers, timeout=10, stream=True)
            
            if response.status_code != 200:
                print(f"❌ 下载失败：{img_url}")
                return False
            
            # 获取文件名
            filename = os.path.basename(img_url)
            if not filename:
                filename = f"image_{int(time.time())}.jpg"
            
            # 保存图片
            filepath = os.path.join(save_path, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            print(f"✅ 已保存：{filename}")
            return True
            
        except Exception as e:
            print(f"❌ 下载失败：{img_url} - {e}")
            return False
    
    def run(self, url):
        """
        运行爬虫
        """
        print(f"🚀 开始爬取：{url}")
        
        # 获取所有图片URL
        img_urls = self.get_all_images(url)
        
        if not img_urls:
            print("❌ 没有找到图片！")
            return
        
        # 下载图片
        print(f"📥 开始下载 {len(img_urls)} 张图片...")
        success_count = 0
        
        for idx, img_url in enumerate(img_urls, 1):
            print(f"\n[{idx}/{len(img_urls)}] 正在下载：{img_url}")
            if self.download_image(img_url, self.save_path):
                success_count += 1
        
        print(f"\n🎉 下载完成！成功下载 {success_count}/{len(img_urls)} 张图片")
        print(f"📂 图片保存路径：{self.save_path}")

if __name__ == "__main__":
    # 爬取目标URL
    target_url = "https://www.ihuiwa.com/workspace/ai-image/wear-everything"
    
    # 创建爬虫
    crawler = IHuiwaImageCrawler()
    
    # 运行爬虫
    crawler.run(target_url)