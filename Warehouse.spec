# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Volumes/2ndev-T7/UIT/Python/warehouse/app/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Volumes/2ndev-T7/UIT/Python/warehouse/app', 'app'), ('/Volumes/2ndev-T7/UIT/Python/warehouse/resources', 'resources')],
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
    [],
    exclude_binaries=True,
    name='Warehouse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity='',
    entitlements_file=None,
    icon=['resources/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Warehouse',
)
app = BUNDLE(
    coll,
    name='Warehouse.app',
    icon='resources/icon.icns',
    bundle_identifier='com.warehouse.app',
)
