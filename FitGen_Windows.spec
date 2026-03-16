# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# 获取项目路径
project_path = os.path.abspath(os.path.dirname(SPECPATH))

a = Analysis(
    ['launcher.py'],
    pathex=[project_path],
    binaries=[],
    datas=[
        # 包含后端代码
        ('backend/app.py', 'backend'),
        ('backend/.env', 'backend'),
        # 包含前端代码
        ('frontend/app.py', 'frontend'),
        # 包含静态文件
        ('backend/files', 'backend/files'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'streamlit',
        'aiohttp',
        'PIL',
        'pydantic',
        'starlette',
        'requests',
        # Streamlit 依赖
        'streamlit.runtime',
        'streamlit.web.server',
        'altair',
        'pandas',
        'numpy',
        'tornado',
        'click',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'tkinter', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FitGen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
