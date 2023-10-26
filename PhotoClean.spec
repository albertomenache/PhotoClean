# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:/Users/alberto/Documents/Dev/VisionData/PhotoClean'],
    binaries=[],
    datas=[('main.ui', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

a.datas += [('icons/arrow-left.png','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/arrow-left.png', "DATA")]
a.datas += [('icons/arrow-right.png','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/arrow-right.png', "DATA")]
a.datas += [('icons/download.png','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/download.png', "DATA")]
a.datas += [('icons/folder-open.png','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/folder-open.png', "DATA")]
a.datas += [('icons/Icon.ico','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/Icon.ico', "DATA")]
a.datas += [('icons/loop2.png','C:/Users/alberto/Documents/Dev/VisionData/PhotoClean/icons/loop2.png', "DATA")]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PhotoClean',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    hide_console='hide-early',
)
