# -*- coding: utf-8 -*-

## 必要なモジュールをインポート
import os
import sys

## PySide系モジュール
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import QUiLoader

from MasterOfMainWindow import MasterOfMainWindow
from UI_SignalAnalyser_a01 import Ui_MainWindow

## uiファイル名
# uiFile = 'UI_SignalAnalyser_a01.ui'



# =============================================================================
## GUIの構築
class GUI(QMainWindow, Ui_MainWindow):
# class GUI(MasterOfMainWindow):

    def __init__(self, parent=None):
        # super(GUI).__init__(self)
        QMainWindow.__init__(self)
        # print type(self)
        Ui_MainWindow.__init__(self)
        pass





# =============================================================================
## GUIの起動
def main():
    app = QApplication(sys.argv)
    wnd = GUI()
    wnd.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    # -----------------------------------------------------------------------------
    # EOF
    # -----------------------------------------------------------------------------
