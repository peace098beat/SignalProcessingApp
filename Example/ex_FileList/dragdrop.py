## -*- coding: utf-8 -*-
import sys
import re

from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader

import remitools.lib.qt as remiQt


class dragdrop(QtGui.QDialog):
    """
    UIにドラッグ＆ドロップしたファイル一覧をListに表示する
    """
    uiFile = "dragdrop.ui"

    def __init__(self):

        super(dragdrop, self).__init__(remiQt.getMayaWindow())

        self.ui = remiQt.getWidget(self.uiFile, self)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        # ドロップ許可
        self.setAcceptDrops(True)

    def dropEvent(self, event):

        """
        ドラッグされたオブジェクトの、ドロップ許可がおりた場合の処理
        """
        mimedata = event.mimeData()
        urllist = mimedata.urls()

        # 一度クリアした後、ドラッグしたファイルの一覧をListに追加する
        self.ui.listWidget.clear()
        for i in urllist:
            self.ui.listWidget.addItem(re.sub("^/", "", i.path()))

    def dragEnterEvent(self, event):

        """
        ドラッグされたオブジェクトを許可するかどうかを決める
        ドラッグされたオブジェクトが、ファイルなら許可する
        """
        mime = event.mimeData()

        if mime.hasUrls() == True:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = dragdrop()
    app.show()
