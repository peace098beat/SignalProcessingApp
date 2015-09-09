#! coding:utf-8
"""
QListViewを使って、ファイルをリストする

PySideでリストをカスタマイズするぞ！　～基礎編「model/viewアーキテクチャ」～
http://www.dfx.co.jp/dftalk/?p=14388

PySideでリストをカスタマイズするぞ！　～応用編「delegate」～
http://www.dfx.co.jp/dftalk/?p=16745

"""

import sys
import os
import warnings
from PySide.QtCore import *
from PySide.QtGui import *


class CustomListModel(QAbstractListModel):
    """ データを格納するモデルクラス
    リストに表示するデータ名だけでなく、その他の情報も持っていられる。
    返却時に指定されたデータを渡す
    """

    def __init__(self, parent=None, data=[]):
        super(CustomListModel, self).__init__(parent)
        self.__items = data

    def clearItems(self):
        self.__items = []

    def addItem(self, data):
        self.__items.append(data)

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
            color = self.__items[index.row()].get("color", [])
            return QColor(*color)

        # 背景色を返却
        elif role == Qt.BackgroundRole:
            color = self.__items[index.row()].get("bgcolor", [])
            return QColor(*color)

        # Thumbnailキーの画像ファイル名を返す
        elif role == Qt.UserRole:
            return self.__items[index.row()].get("thumbnail", "")

        else:
            return None


class CustomListDelegate(QStyledItemDelegate):
    """オリジナルのデリゲータ
    Listの表示を任意にできるが、Delegateを使うとデフォルトのカラー等は反映されなくなる
    """

    THUMB_WIDTH = 30
    MARGIN = 5
    def __init__(self, parent=None):
        super(CustomListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        '''(継承メソッド)'''
        CURRENT_PATH = os.curdir

        # 背景色の変更
        # ===================
        bgColor = QColor(60, 60, 60)
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
        color = index.data(Qt.ForegroundRole)
        thumbName = index.data(Qt.UserRole)

        # サムネイル画像の表示
        # ========================
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
        # ペンを持たせる
        pen = QPen(color, 0.5, Qt.SolidLine)
        painter.setPen(pen)

        # テキストを描く
        r = QRect(option.rect.left() + self.THUMB_WIDTH + self.MARGIN,
                  option.rect.top(),
                  option.rect.width() - self.THUMB_WIDTH - self.MARGIN,
                  option.rect.height())
        painter.drawText(r,
                         Qt.AlignVCenter | Qt.AlignLeft,
                         "Name:" + name)


    def sizeHint(self, option, index):
        return QSize(100, self.THUMB_WIDTH)


def main2():
    app = QApplication(sys.argv)
    data = [
        {"name": "Lion", "color": [237, 111, 112], "thumbnail": "ball2.png"},
        {"name": "Monkey", "color": [127, 197, 195], "thumbnail": "ball3.png"}
    ]
    myListModel = CustomListModel(data=data)
    myListDelegete = CustomListDelegate()

    # QListViewを使うためには下のコードを書くだけ
    myListView = QListView()
    myListView.setModel(myListModel)
    myListView.setItemDelegate(myListDelegete)
    # ===========================================

    myListView.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main2()
