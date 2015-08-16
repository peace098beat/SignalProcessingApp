#! encoding:utf-8
"""
MasterOfMainWindow.py

使い方

ステータスバー
self.statusBar().showMessage("File saved", 2000)

"""
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *

# =============================================================================
## MasterOfMainWindow
class MasterOfMainWindow(QMainWindow):
    """ Our Main Window Class
    """
    # fileloaded = Signal()
    fileloaded = Signal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon('./FiSig/icon/icon_fifi.png'))

        # ====================================
        # メンバ変数の定義
        # ====================================
        self.fileName = None
        # パス名 path の正規化された絶対パスを返します。
        self.abspath = None
        # パス名 path の末尾のファイル名部分を返します。
        self.basename = None
        # パス名 path のディレクトリ名を返します。
        self.dirname = None
        # pathが実在するパスか、オープンしているファイル記述子を参照している場合 True を返します。
        self.exists = None
        # 拡張子無しファイル名と、拡張子を返す
        self.name, self.ext = None, None

    ##############################################
    # スロット
    ##############################################
    @Slot()
    def openFileDialog(self):
        """ ファイルオープンダイアログの表示
        """
        fname, filt = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Wave Files (*.wav);; All Files (*)')
        # print 'openFileDialog loadfile', str(fname)

        # 呼び出したファイルの格納
        self.cahangeFilePath(fname)

    ##############################################
    # ドラッグアンドドロップのイベント処理
    ##############################################
    def dragEnterEvent(self, event):
        """ドラッグイベントの検知
        """
        print 'dragEnterEvent'
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """ドロップイベントの検知
        ..Todo: フォルダ内ファイルの読み込み対応
        """
        print 'dropEvent'
        files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
        for fname in files:
            print 'dropEvent::', type(fname)
            # print str(fname)

        # 呼び出したファイルを格納
        file = files[0]
        self.cahangeFilePath(fname)

    ##############################################
    #
    # cahangeFilePath
    #   ファイルが呼び出された後の処理
    #  1. ファイルオープンダイアログ
    #  2. drag&drop
    ##############################################
    def cahangeFilePath(self, filepath):
        """ 読み込んだファイル名をメンバ変数に格納し、シグナルを発行
                """
        # 文字コードの保障
        if not isinstance(filepath, unicode):
            filepath = unicode(filepath)

        # パスを整理し、メンバ変数に格納
        self.parseFilename(filepath)

        # シグナルの発行
        self.fileloaded.emit(self.name)

    ##############################################
    # サブ関数:: ファイル名をパースし保管
    ##############################################
    def parseFilename(self, filepath):
        import os.path

        # パス名 path の正規化された絶対パスを返します。
        self.abspath = os.path.abspath(filepath)
        # パス名 path の末尾のファイル名部分を返します。
        self.basename = os.path.basename(filepath)
        # パス名 path のディレクトリ名を返します。
        self.dirname = os.path.dirname(filepath)
        # pathが実在するパスか、オープンしているファイル記述子を参照している場合 True を返します。
        self.exists = os.path.exists(filepath)
        # 拡張子無しファイル名と、拡張子を返す
        self.name, self.ext = os.path.splitext(self.basename)

        print "------------- fileloaded ----------------"
        print "abspath", type(self.abspath), str(self.abspath)
        print "basename", type(self.basename), str(self.basename)
        print "dirname", type(self.dirname), str(self.dirname)
        print "exists", type(self.exists), str(self.exists)
        print "name", type(self.name), str(self.name)
        print "ext", type(self.ext), str(self.ext)
        print "Please help SimpleFileLoader"
        print "-----------------------------------------"




# =============================================================================
## DEMO
if __name__ == '__main__':
    # Exception Handling
    try:
        myApp = QApplication(sys.argv)
        mainWindow = MasterOfMainWindow()
        mainWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------