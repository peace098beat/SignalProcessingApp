#! encoding:utf-8
"""
gui_fileListWidget.py

Description:
    ドラッグアンドドロップでファイルリストを表示するウィジェット
    本当のデータはmodelが格納している。
    Delegeteはリストのindex毎にModeからデータを読み出している。

Example:
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)

        data = [
            {u"name":u"file1.wav"},
            {u"name":u"file2.wav"}
        ]

        # モデルとデリゲートを生成
        self.myListModel = CustomListModel(data=data)
        self.myListDelegete = CustomListDelegate()

        # QListViewを使うためには下のコードを書くだけ
        self.myListView = QListView()
        self.myListView.setModel(self.myListModel)
        self.myListView.setItemDelegate(self.myListDelegete)

        # UI配置
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.myListView)
        self.setCentralWidget(self.widget)

    # ドラッグアンドドロップのイベント処理
    def dragEnterEvent(self, event):
        #ドラッグイベントの検知

        print 'dragEnterEvent'
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        #ドロップイベントの検知
        print 'dropEvent'

        # リストのクリア
        self.myListModel.clearItems()

        files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
        for fname in files:
            # print 'dropEvent::', type(fname)
            f = os.path.basename(fname)
            self.myListModel.addItem({u"name":f})
            # self.myListModel.clearItems()

"""

import time
import sys
import os
import warnings
from PySide.QtCore import *
from PySide.QtGui import *


# =============================================================================

class CustomListModel(QAbstractListModel):
    """ データを格納するモデルクラス
        リストに表示するデータ名だけでなく、その他の情報も持っていられる。
        返却時に指定されたデータを渡す
        """

    def __init__(self, parent=None, data=[]):
        super(CustomListModel, self).__init__(parent)
        self.__items = data

    def clearItems(self):
        # データのクリア
        self.__items = []

    def addItem(self, data):
        # データを格納
        self.__items.append(data)
        # シグナル発行
        self.dataChanged.emit(0, 1)

    def addItems(self, datas):
        self.clearItems()

        for fname in datas:
            # f = os.path.basename(fname)
            self.addItem({u"name": fname})

    def rowCount(self, parent=QModelIndex()):
        '''行の数(アイテムの数)を返却
        ※ 継承に必要
        '''
        return len(self.__items)

    def data(self, index, role=Qt.DisplayRole):
        '''指定されたデータを返却
        ※ 継承に必要
        例）
            DisplayRole: テキストデータでメインの文字列表示に使われる
            ToolTipRole: ツールチップ（マウスをホバーした際に出る補助テキスト）の表示に使われる
            BackgroundRole: 背景の描画に使われる
            ForegroundRole: 文字の色などに使われる
        '''
        if not index.isValid():
            return None

        # 行番号が境界内に収まっているか
        if not 0 <= index.row() < len(self.__items):
            return None

        # 指定されたデータを返却
        if role == Qt.DisplayRole:
            return self.__items[index.row()].get("name")

        # 文字色を返却
        elif role == Qt.ForegroundRole:
            # color = self.__items[index.row()].get("color", [])
            color = [20, 20, 20]
            return QColor(*color)


        # 背景色を返却
        elif role == Qt.BackgroundRole:
            # color = self.__items[index.row()].get("bgcolor", [])
            color = [20, 20, 20]
            return QColor(*color)

        # Thumbnailキーの画像ファイル名を返す
        elif role == Qt.UserRole:
            # return self.__items[index.row()].get("thumbnail", "")
            return 'ball2.png'

        else:
            return None


# =============================================================================

class CustomListDelegate(QStyledItemDelegate):
    """オリジナルのデリゲータ
    Listの表示を任意にできるが、Delegateを使うとデフォルトのカラー等は反映されなくなる
    """

    THUMB_WIDTH = 20
    MARGIN = 1

    def __init__(self, parent=None):
        super(CustomListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        '''(継承メソッド)'''

        # imgファイルの存在場所を指定
        CURRENT_PATH = os.curdir
        # Thumbnailを使う場合のフラグ
        USE_THUMNAIL = False
        thumbName = 'ball2.png'
        BG_COLOR = [150, 150, 150]
        TXT_COLOR = [100, 10, 100]

        # 背景色の変更
        # ===================
        bgColor = QColor(*BG_COLOR)
        # 選択状態の判定
        if option.state & QStyle.State_Selected:
            # 背景を描く
            bgBrush = QBrush(bgColor)
            bgPen = QPen(bgColor, 0.5, Qt.SolidLine)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            painter.drawRect(option.rect)

        # indexからデータを取り出す
        name = index.data(Qt.DisplayRole)

        # サムネイル画像の表示
        # ========================
        if USE_THUMNAIL:
            imgpath = os.path.join(CURRENT_PATH, "images", thumbName)
            # ファイルの存在確認
            if not os.path.exists(imgpath):
                print('File Not exist')
                warnings.warn('file not exist')

            thumbImage = QPixmap(imgpath).scaled(self.THUMB_WIDTH, self.THUMB_WIDTH)
            # 画像の表示場所を指定
            r = QRect(option.rect.left(), option.rect.top(), self.THUMB_WIDTH, self.THUMB_WIDTH)
            painter.drawPixmap(r, thumbImage)

        # 文字色の変更
        # ==============
        tcolor = QColor(*TXT_COLOR)
        # ペンを持たせる
        pen = QPen(tcolor, 0.5, Qt.SolidLine)
        painter.setPen(pen)

        # テキストを描く
        if USE_THUMNAIL:
            r = QRect(option.rect.left() + self.THUMB_WIDTH + self.MARGIN,
                      option.rect.top(),
                      option.rect.width() - self.THUMB_WIDTH - self.MARGIN,
                      option.rect.height())
        else:
            r = option.rect

        # テキストの表示
        painter.drawText(r,
                         Qt.AlignVCenter | Qt.AlignLeft,
                         "" + os.path.basename(name))

    def sizeHint(self, option, index):
        return QSize(100, self.THUMB_WIDTH)


# =============================================================================
class FileListWidget(QListView):
    """ D&Dでファイルを追加するウィジェット
    """

    def __init__(self, parent=None):
        QListView.__init__(self, parent)
        data = [
            {u"name": u"file1.wav"},
            {u"name": u"file2.wav"}
        ]
        # モデルとデリゲートを生成
        self.myListModel = CustomListModel(data=data)
        self.myListDelegete = CustomListDelegate()
        self.setModel(self.myListModel)
        self.setItemDelegate(self.myListDelegete)

    def clearItems(self):
        self.myListModel.clearItems()

    def addItem(self, data):
        self.myListModel.addItem(data)


# =============================================================================
## MasterOfMainWindow
class MainWindow(QMainWindow):
    """ Our Main Window Class
    """
    fileloaded = Signal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        # self.setWindowIcon(QIcon('./FiSig/icon/icon_fifi.png'))
        # D&Dを使う設定フラグ
        self.setAcceptDrops(True)

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

        # UIの生成
        # ====================================
        # data = [
        #     {u"name": u"file1.wav"},
        #     {u"name": u"file2.wav"}
        # ]
        # モデルとデリゲートを生成
        # self.myListModel = CustomListModel(data=data)
        # self.myListDelegete = CustomListDelegate()

        # QListViewを使うためには下のコードを書くだけ
        # self.myListView = QListView()
        self.myListView = FileListWidget()
        # self.myListView.setModel(self.myListModel)
        # self.myListView.setItemDelegate(self.myListDelegete)

        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(self.myListView)
        self.setCentralWidget(self.widget)

        # ====================================
        # シグナルスロットのコネクト
        # ====================================
        self.connect(self.myListView, SIGNAL("clicked(QModelIndex)"), self.slot1)

    @Slot()
    def slot1(self, index):
        print 'listslot'
        print index.row()
        print index.data(Qt.DisplayRole)
        name = index.data(Qt.DisplayRole)
        self.cahangeFilePath(name)

    ##############################################
    # スロット
    ##############################################
    @Slot()
    def openFileDialog(self):
        """ ファイルオープンダイアログの表示
        """
        fname, filt = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Wave Files (*.wav);; All Files (*)')

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

        urls = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]

        # リストを消去
        # self.myListModel.clearItems()
        self.myListView.clearItem()

        import glob

        # 各URLをリストに追加する
        for url in urls:
            # URLがフォルダかファイルかを判定
            if os.path.isdir(url):
                # パスを正規化
                abspath = os.path.abspath(url)
                print 'This is Dir : ', abspath
                # フォルダ直下の.wavを検索
                searchpath = os.path.join(abspath, '*.wav')
                # ディレクトリ直下のファイルを呼び出す
                files = [r for r in glob.glob(searchpath)]
                # ファイルリストから一つずつリストに追加
                for file in files:
                    # self.myListModel.addItem({u"name": file})
                    self.myListView.addItem({u"name": file})
            else:
                # URLがファイルの場合、(.wav)だけをリストにつか
                abspath = os.path.abspath(url)
                # 拡張子を取得
                name, ext = os.path.splitext(abspath)
                # .wavの場合だけ追加
                if ext == '.wav':
                    # self.myListModel.addItem({u"name": abspath})
                    self.myListView.addItem({u"name": abspath})
                print 'This is not Dir :', abspath

    ##############################################
    # cahangeFilePath
    #   ファイルが呼び出された後の処理
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
        mainWindow = MainWindow()
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
