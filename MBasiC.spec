# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None


a = Analysis(['entrypoint.py'],
             pathex=[],
             binaries=[],
             datas=[(os.path.join(root, file), 'bin') for root, dir, files in os.walk(os.path.join(os.getcwd(), 'static')) for file in files if file.endswith('jar')] + [(os.path.join(root, file), 'resources') for root, dir, files in os.walk(os.path.join(os.getcwd(), 'resources')) for file in files],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='MBasiC',
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
          entitlements_file=None )
