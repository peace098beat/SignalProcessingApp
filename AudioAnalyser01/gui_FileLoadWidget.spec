# -*- mode: python -*-
a = Analysis(['gui_FileLoadWidget.py'],
             pathex=['C:\\Users\\fifi\\Dropbox\\10_GitRepository\\SignalProcessingApp\\AudioAnalyser01'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gui_FileLoadWidget.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
