# plik spec dla pyinstaller - pakuje front.py do .exe
# uzycie: pyinstaller chess.spec

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis

block_cipher = None

a = Analysis(
    ['front.py'],
    pathex=['.'],
    binaries=[],
    # dolacz katalog z obrazkami figur i caly silnik
    datas=[
        ('images', 'images'),
        ('engine', 'engine'),
    ],
    hiddenimports=['pygame', 'engine.Board', 'engine.Manager',
                   'engine.Generator', 'engine.Strategy', 'engine.AI'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['fastapi', 'uvicorn', 'pydantic'],
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
    name='chess',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    # jeden plik exe bez folderu dist
    onefile=True,
    console=False,  # brak okna konsoli
    icon=None,
)
