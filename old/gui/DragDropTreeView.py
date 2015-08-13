# -*- coding:utf-8 -*-
"""DragDropTreeView.py
ドラッグドッロプでファイルの読み込みを行えるように
拡張したツリーウィジェットです。

..Todo: 受け取ったファイルのグローバル変数化
..Todo: ツリーのリセット機能の追加
..Todo: フォルダの場合子供ツリーを作る
"""
import sys
from PyQt4 import QtGui, QtCore


class DragDropItemModel(QtGui.QStandardItemModel):

    '''ドロップ可能なQStandardItemModelの派生クラス。'''

    def __init__(self, parent=None):
        super(DragDropItemModel, self).__init__(0, 1, parent)
        self.setHeaderData(0, QtCore.Qt.Horizontal, 'File Name')
        self.setHeaderData(1, QtCore.Qt.Horizontal, 'File Path')
        self.setHeaderData(2, QtCore.Qt.Horizontal, 'Other')

    def addObject(self, url):
        '''QUrlを受け取って、リストに追加するメソッド。
        ..Todo: Windows対応なのでクロスプラットフォーム化
        '''
        filepath = url.path()
        fileinfo = QtCore.QFileInfo(url.path())
        filename = fileinfo.fileName()

        # filepath = url.path()            # QUrlからパスを取得。

        # Windowsから送られてくるuri-listは頭に/が付いているので
        # それをはずす。
        # filepath = filepath[1:]

        # uri-listはパスの区切り文字が/なので、Windows風に￥に置き換える。
        # filepath = filepath.replace( '/', '\\' )

        # 追加するアイテムを作成。
        row = self.rowCount()

        # ファイルの更新日時のアイテムの追加。
        item = QtGui.QStandardItem()
        item.setText(filename)
        self.setItem(row, 0, item)

        # ファイルパスのアイテムの追加。
        item = QtGui.QStandardItem()
        item.setText(filepath)
        self.setItem(row, 1, item)

        # ファイルのサイズのアイテムを追加。
        # item = QtGui.QStandardItem()
        # item.setText(
        # str( round( fileinfo.size() / 1024.0, 2 ) ) + 'KB'
        # )
        # self.setItem( row, 2, item )

    def mimeData(self, indexes):
        '''ドラッグ先に渡すためのMime Dataを作成し、返す。'''
        mimedata = QtCore.QMimeData()        # Mime Dataを作成。
        urllist = []
        for index in indexes:
            # 渡されたインデックスのColumnが0以外なら処理をスルー。
            if index.column() != 0:
                continue

            item = self.itemFromIndex(index)
            filepath = item.text()
            # Windowsのuri-listは、ファイルのあたまに"/"が必要なため"/"を付加する。
            # またQMimeDataのsetUrlsメソッドはQUrlのリストを要求するため、
            # QUrlにキャストしてからリストに追加。
            urllist.append(QtCore.QUrl('/' + filepath))
        mimedata.setUrls(urllist)

        return mimedata


class DragDropTreeView(QtGui.QTreeView):

    '''ドラッグ＆ドロップ可能なQTreeViewの派生クラス。'''

    def __init__(self, parent=None):
        super(DragDropTreeView, self).__init__(parent)
        self.setDragEnabled(True)            # ドラッグ可能に設定。
        self.setAcceptDrops(True)            # ドロップ可能に設定。
        self.setSortingEnabled(True)  # ソート可能に設定。
        # ドラッグ＆ドロップのモードを指定。
        self.setDragDropMode(
            QtGui.QAbstractItemView.InternalMove
        )
        self.setup_ui()

    def setup_ui(self):
        # カスタムクラスのモデルをセット
        model = DragDropItemModel()
        self.setModel(model)
        # カラムの幅を指定する。
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 100)

    def dragEnterEvent(self, event):
        '''ファイルがこのビューにドラッグされてきた時の挙動を指定。'''
        # 渡されるeventオブジェクトからドラッグされたデータのmimeデータを取得。
        mimedata = event.mimeData()
        if mimedata.hasUrls():
            # ファイルのパス情報を含むmime-type(uri-list)の場合ドロップを許可する
            # 通知を送る。
            event.accept()
        else:
            # それ以外の場合はドロップを無視する通知を送る。
            event.ignore()

    def dropEvent(self, event):
        '''dropを許可して、かつユーザーがこのビューにドロップした場合の処理'''
        mimedata = event.mimeData()

        # このTreeViewにセットされているItemModelを取得する。
        model = self.model()

        if mimedata.hasUrls():
            # QUrlListを取得すし、それをfor文で個別に処理をする。
            urllist = mimedata.urls()
            for url in urllist:
                model.addObject(url)
            event.accept()
        else:
            event.ignore()


if __name__ in '__main__':
    app = QtGui.QApplication(sys.argv)
    # window = MainWindow()
    window = QtGui.QMainWindow()
    window.setCentralWidget(DragDropTreeView())
    window.show()

    sys.exit(app.exec_())
