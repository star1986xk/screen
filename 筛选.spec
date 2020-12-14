# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['筛选.py'],
             pathex=['C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'E:\\screen'],
             binaries=[],
             datas=[],
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
          name='筛选',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='UI\\title.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='筛选')
