# -*- coding: utf-8 -*-
""" MainApplication.py
GUIアプリケーションのワイヤーフレーム。

@authur:    tomoyuki nohara
"""
# PyQt4 imports
from PyQt4 import QtGui, QtCore

from AudioManager import *
from ButtonBoxWidget import *
from DragDropTreeView import *
from GraphBoxWidget import *


# import numpy for generating random data points
# グローバルオブジェクト
# オーディオファイルを操作
# global am
# am = AudioManager()

# PyQt OpenGL
# PyOpenGL


class MainWidget(QtGui.QMainWindow):

    """GUIテンプレート用のメインウィンドウ
    機能
     : メニューバー
     : キーボードショートカット
     : ドラッグ・ドロップに対応
    その他
        実際のウィジェットは別クラスで作成
    """
    width = 1024 / 2
    height = 680

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("FiFiFactory App")
        self.setGeometry(10, 10, self.width, self.height)
        self.resize(self.width, self.height)
        self.setAcceptDrops(True)

        # メニューバーの追加
        # : File->Close
        fileMenu = QtGui.QMenu("&File", self)
        self.action_close = fileMenu.addAction("&Close")
        self.action_close.setShortcut("Ctrl+W")
        self.menuBar().addMenu(fileMenu)
        self.connect(
            self.action_close, QtCore.SIGNAL("triggered()"), self.quit)

        # 背景imageの変更
        # <http://www.cnblogs.com/dcb3688/p/4237204.html>
        palette = QtGui.QPalette(self)
        palette.setColor(self.backgroundRole(), QtGui.QColor(100, 100, 100))
        # palette.setBrush(self.backgroundRole(),
        #   QtGui.QBrush(QtGui.QPixmap('./img/bg1.png')))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def quit(self):
        """アプリ終了
        """
        sys.stdout.write("close.¥n")
        app.quit()

    def keyPressEvent(self, ev):
        """キーボードショートカットの検知
        """
        if ev.key() == QtCore.Qt.Key_Q:
            """Qキーが押されたときTrue
            """
            if(ev.modifiers() and QtCore.Qt.ControlModifier):
                """Cntl+を押しているとき
                """
                sys.stdout.write(u"quit.¥n")
                self.quit()

    def dragEnterEvent(self, event):
        """ドラッグイベントの検知
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """ドロップイベントの検知
        ..Todo: フォルダ内ファイルの読み込み対応
        """
        files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            am.set_wav(f)
            print f


# define a Qt window with an OpenGL widget inside it
class AnalysisPanel(QtGui.QWidget):

    """GUIテンプレート用のパネルウィジェット
    ..Todo: mainから取り出す
    """

    def __init__(self):
        super(AnalysisPanel, self).__init__()
        # global am
        self.am = AudioManager()

        self.setLayout(QtGui.QVBoxLayout())

        ''' user widget '''
        button_box_w = ButtonBoxWidget()
        graph_box_w = GraphBoxWidget(audiomanager=self.am)

        """ * panel_layout(QVBoxLayout) """
        self.layout().addWidget(graph_box_w, 7)
        self.layout().addWidget(button_box_w, 1)

        """ SIGNALの接続 """
        button_box_w.start_button.clicked.connect(self.am.play)
        button_box_w.load_button.clicked.connect(self.open_file)
        button_box_w.plot_button.clicked.connect(graph_box_w.plot)
        button_box_w.analys_button.clicked.connect(graph_box_w.replot_graph)
        
        """ SIGNALの接続(スライダー) """
        button_box_w.slider_low.valueChanged.connect(graph_box_w.chg_range_l)
        button_box_w.slider_high.valueChanged.connect(graph_box_w.chg_range_h)

        self.show()

    def open_file(self):
        print '== open_file:: ='
        file = QtGui.QFileDialog.getOpenFileName()
        if file:
            self.am.set_wav(unicode(file))


if __name__ == '__main__':

    # メイン処理
    app = QtGui.QApplication(sys.argv)
    window = MainWidget()

    # タブにウィジェットを追加
    tabs = QtGui.QTabWidget()
    tabs.addTab(AnalysisPanel(), "Analysis")
    tabs.addTab(DragDropTreeView(), "File")

    window.setCentralWidget(tabs)
    window.show()
    app.exec_()

    # ダミー
    dumy = 1
    dumy = 2
