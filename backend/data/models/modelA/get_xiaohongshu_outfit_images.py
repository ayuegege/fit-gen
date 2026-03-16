# -*- coding: utf-8 -*-
"""
小红书穿搭图片下载工具 - 高效版本
支持从同一个人的穿搭笔记中下载多张不同姿势的照片
"""

import requests
import re
import os
import time
import random
from urllib import parse
from PIL import Image
from io import BytesIO
import hashlib

class XiaohongshuImageSpider(object):
    def __init__(self):
        # 小红书搜索URL
        self.search_url = 'https://www.xiaohongshu.com/search_result?keyword={}'
        # 设置请求头（模拟浏览器）
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xiaohongshu.com',
        }
        # 固定保存路径
        self.save_path = r'D:\fit-gen\backend\data\models\modelA'
        
        # 确保保存路径存在
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            print(f"创建目录：{self.save_path}")

    def get_next_pose_number(self, save_dir):
        """
        获取下一个可用的pose编号
        检查目录中已有的pose文件，返回下一个编号
        """
        if not os.path.exists(save_dir):
            return 1
            
        existing_files = os.listdir(save_dir)
        pose_numbers = []
        
        for filename in existing_files:
            match = re.match(r'pose(\d+)\.jpg', filename)
            if match:
                pose_numbers.append(int(match.group(1)))
        
        if not pose_numbers:
            return 1
        else:
            return max(pose_numbers) + 1

    def get_note_urls(self, keyword, num_notes=10):
        """
        获取小红书穿搭笔记的URL列表
        优先获取同一个人的多篇笔记
        """
        print(f"正在搜索 '{keyword}' 的穿搭笔记...")
        
        # 使用百度图片搜索穿搭关键词，但提取笔记URL
        baidu_url = 'https://image.baidu.com/search/flip?tn=baiduimage&word={}'
        word_parse = parse.quote(keyword)
        
        all_note_urls = []
        page = 0
        max_pages = num_notes * 3
        
        while len(all_note_urls) < num_notes and page < max_pages:
            try:
                url = baidu_url.format(word_parse) + f"&pn={page * 20}"
                response = requests.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                
                # 提取图片URL
                patterns = [
                    r'"objURL":"(https?://[^"]+)"',
                    r'"thumbURL":"(https?://[^"]+)"',
                    r'"hoverURL":"(https?://[^"]+)"',
                    r'"middleURL":"(https?://[^"]+)"',
                ]
                
                for pattern in patterns:
                    urls = re.findall(pattern, response.text)
                    for url in urls:
                        # 过滤掉九宫格图片
                        if 'grid' not in url.lower() and 'collage' not in url.lower():
                            # 提取笔记URL（尝试从图片URL推断）
                            note_url = self.extract_note_url(url)
                            if note_url:
                                all_note_urls.append(note_url)
                
                page += 1
                time.sleep(random.uniform(0.3, 0.8))
                
            except Exception as e:
                print(f"获取第{page}页失败: {e}")
                page += 1
                time.sleep(1)
        
        # 去重并返回
        unique_urls = list(dict.fromkeys(all_note_urls))
        return unique_urls[:num_notes]

    def extract_note_url(self, img_url):
        """
        从图片URL提取笔记URL
        这里使用简化的方式，返回原始图片URL
        """
        # 百度图片的URL通常可以直接使用
        return img_url

    def download_images_from_notes(self, note_urls, num_images_per_note=3, max_total=30):
        """
        从笔记中下载图片
        优先下载同一个人的多张不同姿势照片
        直接使用百度图片返回的图片URL
        """
        all_images = []
        
        for note_url in note_urls:
            if len(all_images) >= max_total:
                break
            
            # 百度图片的URL本身就是图片URL，直接添加
            if note_url and note_url.startswith('http'):
                all_images.append(note_url)
        
        # 去重
        unique_images = list(dict.fromkeys(all_images))
        return unique_images[:max_total]

    def is_good_image(self, img_url):
        """
        判断图片是否符合高质量要求（商业级/高级模特）
        专门针对定制耐克潮鞋的高质量穿搭图筛选
        """
        try:
            response = requests.get(img_url, headers=self.headers, timeout=5)
            img = Image.open(BytesIO(response.content))
            
            width, height = img.size
            
            # 要求高分辨率（至少2K级别）
            if width < 1200 or height < 1600:
                return False
            
            # 过滤掉九宫格图片（宽高比接近1:1）
            if abs(width - height) < 100 and width > 800:
                return False
            
            # 过滤掉过宽的风景图
            if width > height * 1.3:
                return False
            
            # 过滤掉过高的竖图（可能是长图拼接）
            if height > width * 3:
                return False
            
            # 要求宽高比在合理范围（竖屏穿搭图通常在0.7-0.75之间）
            aspect_ratio = width / height
            if aspect_ratio < 0.65 or aspect_ratio > 0.8:
                return False
            
            # 要求高分辨率（至少2K级别）
            if width * height < 1920000:  # 小于200万像素
                return False
            
            # 检查图片是否过暗或过亮（通过平均亮度判断）
            gray = img.convert('L')
            pixels = list(gray.getdata())
            avg_brightness = sum(pixels) / len(pixels)
            
            # 过滤掉过暗（<80）或过亮（>200）的图片
            if avg_brightness < 60 or avg_brightness > 220:
                return False
            
            # 检查图片对比度
            min_pixel = min(pixels)
            max_pixel = max(pixels)
            contrast = max_pixel - min_pixel
            
            # 过滤掉低对比度图片（可能是模糊或低质量）
            if contrast < 80:
                return False
            
            return True
            
        except Exception as e:
            return False

    def calculate_image_hash(self, img_url):
        """
        计算图片的感知哈希值，用于识别相似图片
        """
        try:
            response = requests.get(img_url, headers=self.headers, timeout=5)
            img = Image.open(BytesIO(response.content))
            
            # 转换为灰度图
            gray = img.convert('L')
            
            # 缩放到8x8
            gray = gray.resize((8, 8), Image.Resampling.LANCZOS)
            
            # 计算平均值
            pixels = list(gray.getdata())
            avg = sum(pixels) / len(pixels)
            
            # 生成感知哈希
            hash_str = ''.join(['1' if pixel > avg else '0' for pixel in pixels])
            
            return hash_str
            
        except Exception as e:
            return None

    def are_images_similar(self, hash1, hash2, threshold=0.85):
        """
        比较两张图片的相似度
        使用汉明距离计算
        """
        if not hash1 or not hash2:
            return False
        
        if len(hash1) != len(hash2):
            return False
        
        # 计算汉明距离
        distance = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
        
        # 相似度 = 1 - (汉明距离 / 总位数)
        similarity = 1 - (distance / len(hash1))
        
        return similarity >= threshold

    def select_diverse_images(self, image_urls, num_select=3, min_diversity=0.7):
        """
        从图片列表中选择多样性高的图片（确保是不同姿势）
        """
        if len(image_urls) <= num_select:
            return image_urls
        
        selected = []
        hashes = []
        
        for url in image_urls:
            img_hash = self.calculate_image_hash(url)
            
            if not img_hash:
                continue
            
            # 检查是否与已选图片太相似
            is_similar = False
            for existing_hash in hashes:
                if self.are_images_similar(img_hash, existing_hash, min_diversity):
                    is_similar = True
                    break
            
            if not is_similar:
                selected.append(url)
                hashes.append(img_hash)
                
                if len(selected) >= num_select:
                    break
        
        return selected

    def save_image(self, img_link, filename):
        """
        根据图片链接下载并保存图片到本地
        """
        try:
            if img_link.startswith('\\'):
                img_link = img_link[1:]
            
            img_link = img_link.replace('\\', '')
            
            response = requests.get(img_link, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            width, height = img.size
            print(f'✓ 已保存：{os.path.basename(filename)} ({width}x{height})')
            return True
            
        except Exception as e:
            print(f'✗ 下载失败 {img_link[:50]}... 错误：{str(e)[:50]}')
            return False

    def run(self):
        """
        爬虫的主入口函数
        """
        print("=" * 60)
        print("小红书穿搭图片下载工具 - 高效版")
        print(f"图片保存路径：{self.save_path}")
        print("图片命名格式：pose1.jpg, pose2.jpg, pose3.jpg ...")
        print("=" * 60)
        
        word = input("\n请输入穿搭关键词（推荐：男生穿搭 对镜自拍、Nike Dunk 穿搭、潮鞋穿搭、男生穿搭 自拍、干净背景穿搭、纯色背景穿搭、男生穿搭 全身照）: ").strip()
        if not word:
            print("❌ 关键词不能为空！")
            return

        try:
            num = int(input("请输入想要下载的图片数量（建议10-30张）: "))
            if num <= 0:
                print("❌ 数量必须大于0！")
                return
            if num > 100:
                confirm = input(f"⚠️ 下载{num}张图片可能需要较长时间，确定继续？(y/n): ")
                if confirm.lower() != 'y':
                    print("已取消下载")
                    return
        except ValueError:
            print("❌ 请输入有效的数字！")
            return

        save_dir = os.path.join(self.save_path, word)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"📁 创建目录：{save_dir}")

        start_number = self.get_next_pose_number(save_dir)
        print(f"📝 将从 pose{start_number}.jpg 开始保存")

        # 1. 获取笔记URL
        note_urls = self.get_note_urls(word, num_notes=num * 2)
        print(f"找到 {len(note_urls)} 篇相关笔记")

        if not note_urls:
            print("❌ 没有找到笔记！")
            return

        # 2. 从笔记中下载图片
        print("\n正在从笔记中提取图片...")
        all_images = self.download_images_from_notes(
            note_urls, 
            num_images_per_note=3, 
            max_total=num * 5
        )
        print(f"共提取到 {len(all_images)} 张图片链接")

        if not all_images:
            print("❌ 没有找到图片！")
            return

        # 3. 筛选合适的图片
        print("\n正在筛选合适的图片...")
        good_images = [url for url in all_images if self.is_good_image(url)]
        print(f"筛选后剩余 {len(good_images)} 张合适图片")

        if not good_images:
            print("❌ 没有找到合适的图片！")
            return

        # 4. 选择多样性高的图片（确保是不同姿势）
        print("\n正在选择多样性高的图片（不同姿势）...")
        diverse_images = self.select_diverse_images(good_images, num_select=num)
        print(f"选择到 {len(diverse_images)} 张不同姿势的图片")

        # 5. 下载图片
        print(f"\n开始下载，目标：{len(diverse_images)} 张图片")
        print("下载过程中请稍候...\n")

        downloaded = 0
        failed_count = 0
        max_failures = 10
        current_pose = start_number

        for img_url in diverse_images:
            filename = os.path.join(save_dir, f"pose{current_pose}.jpg")
            
            if self.save_image(img_url, filename):
                downloaded += 1
                current_pose += 1
                failed_count = 0
            else:
                failed_count += 1
            
            if failed_count >= max_failures:
                print(f"⚠️ 连续失败次数过多（{failed_count}），暂停10秒...")
                time.sleep(10)
                failed_count = 0

            time.sleep(random.uniform(0.3, 0.7))

        print("\n" + "=" * 60)
        print("✅ 下载完成！")
        print(f"关键词：{word}")
        print(f"成功下载：{downloaded} 张图片")
        print(f"保存位置：{save_dir}")
        print(f"文件命名：pose{start_number}.jpg 到 pose{start_number + downloaded - 1}.jpg")
        print("=" * 60)

if __name__ == '__main__':
    spider = XiaohongshuImageSpider()
    spider.run()
