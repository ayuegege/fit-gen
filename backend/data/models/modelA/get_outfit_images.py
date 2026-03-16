# -*- coding:utf8 -*-
import requests
import re
import os
from urllib import parse
import time

class BaiduImageSpider(object):
    def __init__(self):
        # 百度图片搜索的URL
        self.url = 'https://image.baidu.com/search/flip?tn=baiduimage&word={}'
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
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
            
        # 获取目录中所有pose文件
        existing_files = os.listdir(save_dir)
        pose_numbers = []
        
        for filename in existing_files:
            # 匹配 pose数字.jpg 格式
            match = re.match(r'pose(\d+)\.jpg', filename)
            if match:
                pose_numbers.append(int(match.group(1)))
        
        if not pose_numbers:
            return 1
        else:
            return max(pose_numbers) + 1

    def get_image_urls(self, url):
        """
        从百度图片搜索结果页中提取图片的下载链接
        """
        try:
            # 发送HTTP请求
            res = requests.get(url, headers=self.headers, timeout=10)
            res.encoding = "utf-8"
            html = res.text

            # 使用正则表达式提取图片的真实URL
            patterns = [
                '"hoverURL":"(.*?)"',
                '"thumbURL":"(.*?)"', 
                '"middleURL":"(.*?)"',
                '"objURL":"(.*?)"'
            ]
            
            img_link_list = []
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.S)
                links = pattern.findall(html)
                if links:
                    img_link_list.extend(links)
                    print(f"找到 {len(links)} 个图片链接")
                    break

            return img_link_list

        except Exception as e:
            print(f"获取图片链接失败：{e}")
            return []

    def save_image(self, img_link, filename):
        """
        根据图片链接下载并保存图片到本地
        """
        try:
            # 处理特殊字符
            if img_link.startswith('\\'):
                img_link = img_link[1:]
            
            # 处理URL中的转义字符
            img_link = img_link.replace('\\', '')

            # 发送请求获取图片
            img_response = requests.get(img_link, headers=self.headers, timeout=10)
            img_response.raise_for_status()

            # 保存图片
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            print(f'✓ 已保存：{os.path.basename(filename)}')
            return True

        except Exception as e:
            print(f'✗ 下载失败，错误：{str(e)[:50]}')
            return False

    def run(self):
        """
        爬虫的主入口函数
        """
        print("=" * 60)
        print("百度穿搭图片下载工具")
        print(f"图片保存路径：{self.save_path}")
        print("图片命名格式：pose1.jpg, pose2.jpg, pose3.jpg ...")
        print("=" * 60)
        
        # 1. 用户输入搜索关键词
        word = input("\n请输入穿搭关键词（如：连衣裙、夏季穿搭、韩系穿搭）: ").strip()
        if not word:
            print("❌ 关键词不能为空！")
            return

        # 2. 用户输入想要下载的图片数量
        try:
            num = int(input("请输入想要下载的图片数量: "))
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

        # 3. 对关键词进行URL编码
        word_parse = parse.quote(word)

        # 4. 创建保存图片的目录
        save_dir = os.path.join(self.save_path, word)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"📁 创建目录：{save_dir}")

        # 5. 获取下一个可用的pose编号
        start_number = self.get_next_pose_number(save_dir)
        print(f"📝 将从 pose{start_number}.jpg 开始保存")

        # 6. 开始下载
        downloaded = 0
        page_num = 0
        failed_count = 0
        max_failures = 10
        current_pose = start_number

        print(f"\n开始搜索 '{word}' 的图片，目标下载数量：{num}")
        print("下载过程中请稍候...\n")

        # 7. 循环翻页下载
        while downloaded < num:
            # 构造每一页的URL
            pn = page_num * 20
            page_url = f"https://image.baidu.com/search/flip?tn=baiduimage&word={word_parse}&pn={pn}"
            
            print(f"正在解析第 {page_num + 1} 页...")
            img_urls = self.get_image_urls(page_url)

            if not img_urls:
                print("❌ 没有获取到图片链接，可能已到达最后一页或被反爬。")
                break

            # 对当前页的每个图片链接进行下载
            page_downloaded = 0
            for i, img_url in enumerate(img_urls):
                if downloaded >= num:
                    break

                # 生成文件名：pose{编号}.jpg
                filename = os.path.join(save_dir, f"pose{current_pose}.jpg")
                
                if self.save_image(img_url, filename):
                    downloaded += 1
                    page_downloaded += 1
                    current_pose += 1  # 编号递增
                    failed_count = 0
                else:
                    failed_count += 1
                    
                # 如果连续失败太多，暂停一下
                if failed_count >= max_failures:
                    print("⚠️ 连续失败次数过多，暂停10秒...")
                    time.sleep(10)
                    failed_count = 0

                # 礼貌地暂停一下
                time.sleep(0.3)

            print(f"第 {page_num + 1} 页完成，本页下载 {page_downloaded} 张，累计 {downloaded}/{num} 张")
            print(f"当前最新编号：pose{current_pose-1 if downloaded>0 else '暂无'}\n")
            
            page_num += 1
            
            if downloaded >= num:
                break
                
            time.sleep(1)

        # 8. 显示最终结果
        print("\n" + "=" * 60)
        print("✅ 下载完成！")
        print(f"关键词：{word}")
        print(f"成功下载：{downloaded} 张图片")
        print(f"保存位置：{save_dir}")
        print(f"文件命名：pose{start_number}.jpg 到 pose{start_number + downloaded - 1}.jpg")
        print("=" * 60)

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()