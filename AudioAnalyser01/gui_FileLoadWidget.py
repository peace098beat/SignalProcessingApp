#! coding:utf-8
"""
FileLoadDlg

ファイルをロードしファイル名を表示するアプリケーション

メンバ変数
    filepath = 絶対パス(C:/Users/fifi/Maschine 2.log)


"""
import sys
from PySide import QtGui, QtCore

class SimpleFileLoader(QtGui.QWidget):

    # ファイルがロードされたときのシグナル
    fileloaded = QtCore.Signal()

    def __init__(self):
        super(SimpleFileLoader, self).__init__()
        self.setAcceptDrops(True)
        self.setupUI()
        self.setupEvent()

    ##############################################
    # UIの作成
    ##############################################
    def setupUI(self):

        self.load_btn = QtGui.QPushButton('Load', self)
        self.load_btn.move(20,10)

        self.fname_label = QtGui.QLabel('no file__________________________________________________________', self)
        self.fname_label.move(100, 10)

        self.play_btn = QtGui.QPushButton('Play', self)
        self.play_btn.move(20, 40)

        # self.setGeometry(0, 0, 1, 80)
        # self.setWindowTitle('SimpleFileLoader')
        # self.show()

    ##############################################
    # シグナル・スロットの作成
    ##############################################
    def setupEvent(self):
        self.load_btn.clicked.connect(self.openFileDialog)
        pass

    ##############################################
    # スロット
    ##############################################
    @QtCore.Slot()
    def openFileDialog(self):
        """ ファイルオープンダイアログの表示
        """
        fname, filt = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Wave Files (*.wav);; All Files (*)')
        print 'openFileDialog loadfile', str(fname)

        # 呼び出したファイルの格納
        self.cahangeFilePath(fname)
    ##############################################
    # サブ関数
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
    # ファイルが呼び出された後の処理
    # ファイルの呼び出し方法は2種類
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

        # ラベルの変更
        self.fname_label.setText(filepath)

        # シグナルの発行
        self.fileloaded.emit()

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

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)



##########################################################
# Example
##########################################################
def main():
    app = QtGui.QApplication(sys.argv)
    w = SimpleFileLoader()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()