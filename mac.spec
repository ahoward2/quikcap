# -*- mode: python ; coding: utf-8 -*-

import sys
import os

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('assets/*', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='QuikCap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True, 
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/QuikCap.icns'],  
)

app = BUNDLE(
    exe,
    name='QuikCap.app',
    icon='assets/QuikCap.icns',
    bundle_identifier='com.ahoward2.quikcap',
)
