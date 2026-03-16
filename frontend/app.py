import streamlit as st
import requests
import time
import json
from PIL import Image
import io
import base64

# 页面配置
st.set_page_config(
    page_title="黑潮AI定制系统",
    page_icon="👟",
    layout="wide"
)

# 自定义CSS - 参考tiancai项目设计风格
st.markdown("""
<style>
    /* 全局样式 - 紫蓝靛渐变背景 */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #581c87 0%, #1e3a8a 50%, #312e81 100%);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }
    
    /* 主容器最大宽度 */
    .block-container {
        max-width: 1280px !important;
        padding-top: 3rem !important;
        padding-bottom: 2rem;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    h1 {
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* 按钮样式 - 粉紫渐变 */
    .stButton>button {
        background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* 禁用状态按钮 */
    .stButton>button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* 毛玻璃卡片样式 */
    .stCard {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Streamlit默认容器优化 - 减少默认间距 */
    div[data-testid="stVerticalBlock"] {
        gap: 0.75rem;
    }
    
    /* 输入框和文件上传器样式 */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.08);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* 文本输入框 */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: #ec4899;
        box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.3);
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }
    
    /* 进度条样式 */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #ec4899 0%, #a855f7 100%);
        border-radius: 9999px;
    }
    
    /* 选择框下拉菜单 */
    [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* 信息提示框样式优化 */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* 成功信息 */
    [data-testid="stAlert"][data-baseweb="notification"] {
        background: rgba(34, 197, 94, 0.2) !important;
        border-color: rgba(34, 197, 94, 0.5) !important;
    }
    
    /* 错误信息 */
    [data-testid="stAlert"][data-baseweb="notification"][kind="error"] {
        background: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
    }
    
    /* 警告信息 */
    [data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
        background: rgba(234, 179, 8, 0.2) !important;
        border-color: rgba(234, 179, 8, 0.5) !important;
    }
    
    /* 信息框 */
    [data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
        background: rgba(59, 130, 246, 0.2) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }
    
    /* 图片容器样式 */
    [data-testid="stImage"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* JSON显示优化 */
    [data-testid="stJson"] {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 后端API地址
API_BASE = "http://127.0.0.1:8000"

# 初始化session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'poses' not in st.session_state:
    st.session_state.poses = []
if 'selected_pose' not in st.session_state:
    st.session_state.selected_pose = None
if 'job_id' not in st.session_state:
    st.session_state.job_id = None
if 'mode' not in st.session_state:
    st.session_state.mode = None

# 模拟数据
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

def show_home():
    """首页 - 选择功能模式"""
    st.markdown("# 👟 黑潮AI定制系统")
    
    # 介绍说明 - 使用毛玻璃卡片
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);margin-bottom:1.5rem;'>
        <p style='text-align:center;color:rgba(255,255,255,0.9);font-size:1.1rem;margin:0;'>
            💡 上传您的鞋子图片，选择合适的模式，一键生成专业级虚拟试鞋效果！
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 三列布局
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;margin-bottom:1rem;'>👗 穿搭替换</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.8);margin-bottom:1.5rem;'>上传穿搭图和鞋子图，一键替换鞋子</p>", unsafe_allow_html=True)
        if st.button("开始穿搭替换", use_container_width=True, key="btn_fashion"):
            st.session_state.page = 'fashion'
            st.session_state.mode = 'fashion'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;margin-bottom:1rem;'>🛍️ 商品展示</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.8);margin-bottom:1.5rem;'>上传鞋子3视图，生成专业商品展示图</p>", unsafe_allow_html=True)
        if st.button("开始商品展示", use_container_width=True, key="btn_product"):
            st.session_state.page = 'product'
            st.session_state.mode = 'product'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;margin-bottom:1rem;'>🎨 AI创意模板</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:rgba(255,255,255,0.8);margin-bottom:1.5rem;'>上传鞋子3视图，生成AI创意设计模板</p>", unsafe_allow_html=True)
        if st.button("开始AI创意", use_container_width=True, key="btn_creative"):
            st.session_state.page = 'creative'
            st.session_state.mode = 'creative'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_fashion_mode():
    """穿搭替换模式"""
    st.markdown("# 👗 穿搭替换 - 黑潮AI定制")

    # 返回按钮
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()

    # 双列布局
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);'>
            <h2 style='margin-top:0;margin-bottom:1rem;'>👗 选择穿搭图</h2>
            <p style='color:rgba(255,255,255,0.8);margin-bottom:1rem;'>💡 从预设的男鞋穿搭 OOTD 中选择3张穿搭图，或者上传自己的穿搭图。</p>
        </div>
        """, unsafe_allow_html=True)

        # 标签页切换
        tab1, tab2 = st.tabs(["📚 预设穿搭图", "📤 自定义上传"])

        with tab1:
            # 获取预设穿搭图列表
            try:
                response = requests.get(f"{API_BASE}/api/poses")
                if response.status_code == 200:
                    poses = response.json()

                    st.markdown("### 请选择3张穿搭图：")

                    # 显示穿搭图选择器
                    selected_poses = []
                    cols = st.columns(3)
                    for i, pose in enumerate(poses):
                        with cols[i]:
                            # 获取完整URL
                            pose_url = f"{API_BASE}{pose['url']}"

                            # 使用 checkbox 让用户选择
                            selected = st.checkbox(
                                f"{pose['name']}",
                                key=f"pose_{pose['id']}",
                                value=False
                            )

                            # 显示图片
                            st.image(pose_url, width=180, caption=pose['name'])

                            if selected:
                                selected_poses.append({
                                    "url": pose_url,
                                    "file_type": "image"
                                })

                    # 保存选择的穿搭图到 session state
                    if selected_poses:
                        st.session_state.selected_poses = selected_poses
                        st.success(f"✅ 已选择 {len(selected_poses)} 张穿搭图")
                        if len(selected_poses) != 3:
                            st.warning(f"⚠️ 请选择3张穿搭图，当前已选择 {len(selected_poses)} 张")
                else:
                    st.error("无法获取穿搭图列表")
            except Exception as e:
                st.error(f"获取穿搭图失败：{str(e)}")

        with tab2:
            outfit_images = st.file_uploader("上传穿搭图（1-3张）", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="outfit_uploader")

            # 保存穿搭图数据到session state
            if outfit_images and len(outfit_images) > 0:
                if 'outfit_images' not in st.session_state or st.session_state.get('last_outfit_count', 0) != len(outfit_images):
                    st.session_state.outfit_images = []
                    for img in outfit_images:
                        img.seek(0)
                        img_bytes = img.read()
                        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                        img_type = img.type.split('/')[1]
                        st.session_state.outfit_images.append({
                            'name': img.name,
                            'type': img.type,
                            'bytes': img_bytes,
                            'image': Image.open(io.BytesIO(img_bytes)),
                            'api_format': {
                                "url": f"data:image/{img_type};base64,{img_base64}",
                                "file_type": "image"
                            }
                        })
                    st.session_state.last_outfit_count = len(outfit_images)
                    st.success(f"✅ 已上传 {len(outfit_images)} 张自定义穿搭图")

            # 显示已上传的穿搭图预览
            if 'outfit_images' in st.session_state and len(st.session_state.outfit_images) > 0:
                st.markdown("### 📷 已上传的穿搭图:")
                cols_outfit = st.columns(min(len(st.session_state.outfit_images), 3))
                for i, img_data in enumerate(st.session_state.outfit_images):
                    with cols_outfit[i]:
                        st.image(img_data['image'], width=200, caption=img_data['name'])
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);'>
            <h2 style='margin-top:0;margin-bottom:1rem;'>👟 上传鞋子图片</h2>
            <p style='color:rgba(255,255,255,0.8);margin-bottom:1rem;'>💡 上传鞋子的1-3张不同视角图片（侧面图、45度图、顶面图）以获得最佳效果。</p>
        </div>
        """, unsafe_allow_html=True)
        
        shoe_images = st.file_uploader("上传鞋子图片（1-3张，不同视角）", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="shoe_uploader")
        
        # 保存鞋子图片数据到session state
        if shoe_images and len(shoe_images) > 0:
            if 'shoe_images_outfit' not in st.session_state or st.session_state.get('last_shoe_count_outfit', 0) != len(shoe_images):
                st.session_state.shoe_images_outfit = []
                for img in shoe_images:
                    img.seek(0)
                    img_bytes = img.read()
                    st.session_state.shoe_images_outfit.append({
                        'name': img.name,
                        'type': img.type,
                        'bytes': img_bytes,
                        'image': Image.open(io.BytesIO(img_bytes))
                    })
                st.session_state.last_shoe_count_outfit = len(shoe_images)
        
        # 显示已上传的鞋子图片预览
        if 'shoe_images_outfit' in st.session_state and len(st.session_state.shoe_images_outfit) > 0:
            st.markdown("### 📷 已上传的鞋子图片:")
            cols_shoe = st.columns(min(len(st.session_state.shoe_images_outfit), 3))
            for i, img_data in enumerate(st.session_state.shoe_images_outfit):
                with cols_shoe[i]:
                    st.image(img_data['image'], width=200, caption=img_data['name'])
    
    # 生成按钮 - 居中显示
    st.markdown("<div style='text-align:center;margin-top:2rem;'>", unsafe_allow_html=True)
    if st.button("✨ 生成穿搭替换图片", use_container_width=True):
        # 检查穿搭图来源
        processed_outfit = []

        # 优先使用预设穿搭图
        if 'selected_poses' in st.session_state and len(st.session_state.selected_poses) == 3:
            processed_outfit = st.session_state.selected_poses
            st.info("📚 使用预设穿搭图")
        # 否则使用自定义上传的穿搭图
        elif 'outfit_images' in st.session_state and len(st.session_state.outfit_images) > 0:
            processed_outfit = [img['api_format'] for img in st.session_state.outfit_images]
            st.info("📤 使用自定义穿搭图")
        else:
            st.error("请选择3张预设穿搭图或上传穿搭图！")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # 检查穿搭图数量
        if len(processed_outfit) != 3:
            st.error(f"请选择3张穿搭图，当前已选择 {len(processed_outfit)} 张")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # 检查鞋子图片
        if 'shoe_images_outfit' not in st.session_state or len(st.session_state.shoe_images_outfit) == 0:
            st.error("请至少上传一张鞋子图片！")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # 处理鞋子图片
        processed_shoes = []
        for img_data in st.session_state.shoe_images_outfit:
            img_base64 = base64.b64encode(img_data['bytes']).decode('utf-8')
            img_type = img_data['type'].split('/')[1]
            processed_shoes.append({
                "url": f"data:image/{img_type};base64,{img_base64}",
                "file_type": "image"
            })

        # 调用API
        try:
            with st.spinner("正在生成，请稍候..."):
                response = requests.post(
                    f"{API_BASE}/api/outfit-replacement",
                    json={
                        "outfit_images": processed_outfit,
                        "shoe_images": processed_shoes
                    }
                )

                st.markdown("## 📊 API响应")
                final_result = response.json()
                st.json(final_result)

                # 显示生成结果
                if final_result and 'output' in final_result:
                    output = final_result['output']
                    if 'result_images' in output:
                        st.markdown("## 🎨 生成结果")
                        result_images = output['result_images']
                        cols = st.columns(min(len(result_images), 3))
                        for i, img_info in enumerate(result_images):
                            with cols[i]:
                                st.image(img_info['url'], caption=img_info.get('style_desc', f'结果 {i+1}'), width=300)
                elif final_result:
                    st.warning("生成结果格式可能与预期不同，请检查响应结构")

        except Exception as e:
            st.error(f"请求失败：{str(e)}")
            import traceback
            st.error(traceback.format_exc())

        time.sleep(1)
        st.markdown("</div>", unsafe_allow_html=True)

def show_product_mode():
    """商品展示生成"""
    st.markdown("# 🛍️ 商品展示生成")
    
    # 返回按钮
    if st.button("🏠 返回首页", use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.job_id = None
        st.rerun()
    
    # 上传鞋子图片 - 使用毛玻璃卡片
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);margin-bottom:1.5rem;'>
        <h2 style='margin-top:0;margin-bottom:1rem;'>📸 上传鞋子图片</h2>
        <p style='color:rgba(255,255,255,0.8);margin-bottom:1rem;'>💡 上传鞋子的1-3张不同视角图片（侧面图、45度图、顶面图）以获得最佳效果。</p>
    </div>
    """, unsafe_allow_html=True)
    shoe_images = st.file_uploader("上传鞋子图片（1-3张，不同视角）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    # 保存图片数据到session state
    if shoe_images and len(shoe_images) > 0:
        if 'uploaded_images' not in st.session_state or st.session_state.get('last_upload_count', 0) != len(shoe_images):
            st.session_state.uploaded_images = []
            for img in shoe_images:
                img.seek(0)
                img_bytes = img.read()
                st.session_state.uploaded_images.append({
                    'name': img.name,
                    'type': img.type,
                    'bytes': img_bytes,
                    'image': Image.open(io.BytesIO(img_bytes))
                })
            st.session_state.last_upload_count = len(shoe_images)
    
    # 显示已上传的图片预览
    if 'uploaded_images' in st.session_state and len(st.session_state.uploaded_images) > 0:
        st.markdown("### 📷 已上传的图片:")
        cols = st.columns(min(len(st.session_state.uploaded_images), 3))
        for i, img_data in enumerate(st.session_state.uploaded_images):
            with cols[i]:
                st.image(img_data['image'], width=200, caption=img_data['name'])
    
    # 生成按钮
    if st.button("✨ 生成商品展示图片", use_container_width=True):
        if 'uploaded_images' not in st.session_state or len(st.session_state.uploaded_images) == 0:
            st.error("请至少上传一张鞋子图片！")
            return
        
        # 处理图片
        processed_images = []
        for img_data in st.session_state.uploaded_images:
            # 转换为Base64 - 使用标准的data URL格式
            img_base64 = base64.b64encode(img_data['bytes']).decode('utf-8')
            img_type = img_data['type'].split('/')[1]
            processed_images.append({
                "url": f"data:image/{img_type};base64,{img_base64}",
                "file_type": "image"  # 统一设置为"image"类型，符合API要求
            })
        
        # 调用API
        try:
            response = requests.post(
                "http://localhost:8000/api/product-replacement",
                json={
                    "shoe_images": processed_images
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success("请求成功！")
                
                # 显示结果
                st.markdown("## 📊 API响应")
                st.json(result)
                
                # 检查是否有错误信息
                if "result" in result:
                    if isinstance(result["result"], dict):
                        # 检查是否有错误信息
                        if "msg" in result["result"]:
                            st.error(f"API返回错误：{result['result']['msg']}")
                        elif "output" in result["result"] and "result_images" in result["result"]["output"]:
                            # 正常显示图片 - stream_run返回格式
                            result_images = result["result"]["output"]["result_images"]
                            st.markdown("## 🎨 生成结果")
                            # 创建三列布局显示图片
                            cols = st.columns(3)
                            for i, img_data in enumerate(result_images):
                                col_idx = i % 3
                                with cols[col_idx]:
                                    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                                    st.image(
                                        img_data["url"], 
                                        caption=f"商品展示图 {i+1} - {img_data.get('style_desc', '')}", 
                                        width=200
                                    )
                                    st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info("生成结果格式可能与预期不同，请检查响应结构")
                    elif isinstance(result["result"], list):
                        # 正常显示图片
                        st.markdown("## 🎨 生成结果")
                        for i, img_url in enumerate(result["result"], 1):
                            st.image(img_url, caption=f"商品展示图 {i}", width=200)
                    else:
                        st.info("生成结果格式可能与预期不同，请检查响应结构")
                else:
                    st.info("未找到result字段，请检查API响应")
            else:
                st.error(f"请求失败：{response.text}")
                
        except Exception as e:
            st.error(f"请求异常：{str(e)}")
            st.exception(e)  # 显示完整异常信息

def show_creative_mode():
    """AI创意模板模式"""
    st.markdown("# 🎨 AI创意模板")
    
    # 返回按钮
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()
    
    # 主界面 - 上传鞋子图片 - 使用毛玻璃卡片
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1);backdrop-filter: blur(16px);border-radius:16px;padding:1.5rem;border:1px solid rgba(255,255,255,0.15);margin-bottom:1.5rem;'>
        <h2 style='margin-top:0;margin-bottom:1rem;'>📤 上传鞋子图片</h2>
        <p style='color:rgba(255,255,255,0.8);margin-bottom:0;'>💡 <strong>提示</strong>：上传一张鞋子图片，生成4种AI创意涂鸦效果。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 上传鞋子图片
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.markdown("### 👟 鞋子图片")
    shoe_file = st.file_uploader("上传鞋子图片", type=['png', 'jpg', 'jpeg'], key="shoe_creative")
    
    if shoe_file:
        image = Image.open(shoe_file)
        st.image(image, width=300, caption="已上传的鞋子图片")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 生成按钮
    if st.button("✨ 生成AI创意模板", use_container_width=True):
        if not shoe_file:
            st.error("请上传鞋子图片！")
            return
        
        # 处理图片
        img_bytes = shoe_file.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        img_type = shoe_file.type.split('/')[1]
        processed_shoe = {
            "url": f"data:image/{img_type};base64,{img_base64}",
            "file_type": "image"
        }
        
        # 调用API
        try:
            with st.spinner("正在生成，请稍候..."):
                response = requests.post(
                    f"{API_BASE}/api/creative-template",
                    json={
                        "shoe_image": processed_shoe
                    }
                )
                
                st.markdown("## 📊 API响应")
                final_result = response.json()
                st.json(final_result)
                
                # 显示生成结果
                if final_result and 'output' in final_result:
                    output = final_result['output']
                    
                    # 显示总结
                    if 'summary' in output:
                        st.markdown(f"## 📝 {output['summary']}")
                    
                    # 显示涂鸦图片
                    if 'doodle_images' in output:
                        st.markdown("## 🎨 生成结果")
                        doodle_images = output['doodle_images']
                        style_names = ["线条艺术", "波点几何", "花卉涂鸦", "抽象艺术"]
                        
                        cols = st.columns(min(len(doodle_images), 4))
                        for i, img_url in enumerate(doodle_images):
                            with cols[i]:
                                style_name = style_names[i] if i < len(style_names) else f'风格 {i+1}'
                                st.image(img_url, caption=style_name, width=250)
                    
                    # 显示PDF下载链接
                    if 'pdf_url' in output:
                        st.markdown("## 📄 PDF文档")
                        st.markdown(f"[下载PDF文档]({output['pdf_url']})")
                elif final_result:
                    st.warning("生成结果格式可能与预期不同，请检查响应结构")
        
        except Exception as e:
            st.error(f"请求失败：{str(e)}")
            import traceback
            st.error(traceback.format_exc())

# 页面导航
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'fashion':
    show_fashion_mode()
elif st.session_state.page == 'product':
    show_product_mode()
elif st.session_state.page == 'creative':
    show_creative_mode()