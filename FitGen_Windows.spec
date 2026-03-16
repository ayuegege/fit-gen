# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

project_path = os.path.abspath(os.path.dirname(SPECPATH))

a = Analysis(
    ['launcher.py'],  # 只打包启动器
    pathex=[project_path],
    binaries=[],
    datas=[
        # 只包含必需的数据文件
        ('backend/files', 'backend/files'),
        ('backend/.env', 'backend'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块
        'matplotlib', 'tkinter', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'PIL', 'numpy', 'pandas',  # 不打包这些，让用户自己安装
    ],
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
