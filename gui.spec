# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['C:\\Users\\roman\\OneDrive\\Desktop\\pythonProjects\\YtDownloader'],
             binaries=[],
             datas=[('download.ico', '.'), ('discover.png', '.'), ('headphone.png', '.'), ('search.png', '.'), ('downloading.png', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='C:\\Users\\roman\\OneDrive\\Desktop\\pythonProjects\\YtDownloader\\download.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='gui')
