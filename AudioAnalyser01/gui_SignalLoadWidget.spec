# -*- mode: python -*-
a = Analysis(['gui_SignalLoadWidget.py'],
             pathex=['C:\\Users\\fifi\\Dropbox\\10_GitRepository\\SignalProcessingApp\\AudioAnalyser01'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gui_SignalLoadWidget.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='gui_SignalLoadWidget')
