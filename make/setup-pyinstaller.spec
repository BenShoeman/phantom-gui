# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os

source_file = '..\\main.py'
base_dir = os.path.dirname(os.path.abspath(source_file))
setup_dir = os.path.join(base_dir, 'make')

a = Analysis([source_file],
             pathex=[setup_dir],
             binaries=[],
             datas=[
			    (os.path.join(base_dir,'bin'),"bin"),
				(os.path.join(base_dir,'html'),"html")
		     ],
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
          name='Phantom-GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='phantom.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Phantom-GUI')
