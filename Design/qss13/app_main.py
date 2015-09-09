#! coding:utf-8
# app_main.py
import os
import sys
from PySide import QtGui, QtUiTools
from qcss13 import qcss13

## Import UI File
UI_FILE_NAME = '/qss13.ui'

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # CSSをインポート
    app.setStyleSheet(qcss13())
    # Ui Loader
    loader = QtUiTools.QUiLoader()
    # Ui ファイルを読み込んでオブジェクトを取得
    ui = loader.load(os.path.dirname(os.path.abspath(sys.argv[0])) + UI_FILE_NAME)
    ui.show()
    sys.exit(app.exec_())
