# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, PYZ, EXE

block_cipher = None
project_root = os.getcwd()

# Collect assets
assets_src = os.path.join(project_root, 'assets')

# Collect pywebview dependencies
pywebview_data, pywebview_bins, pywebview_hidden = collect_all('webview')

hiddenimports = [
    'webview',
    'webview.platforms.winforms',
    'clr',
    'pythonnet',
]
hiddenimports.extend(pywebview_hidden)

datas = [(assets_src, 'assets')]
for item in pywebview_data:
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        datas.append((item[0], item[1]))

binaries = list(pywebview_bins)

a = Analysis(
    [os.path.join(project_root, 'main.py')],
    pathex=[project_root],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='AntiAfkBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    onefile=True,
)
