#-*- coding:utf-8
"""
treeを表示するために
modeとviewを分けて考えるチュートリアル。

共通のモデルを、異なるビューで表示している。
http://www.dfx.co.jp/dftalk/?p=14388

"""
import sys
from PySide import QtCore, QtGui
 
def main():
    app = QtGui.QApplication(sys.argv)
 
    # modelの生成
    myListModel = QtGui.QStringListModel(["Lion", "Monkey", "Tiger", "Cat"])

    # Viewの生成
    myListView1 = QtGui.QListView()
    myListView2 = QtGui.QListView()
 
    # リストにmodelをセット
    myListView1.setModel(myListModel)
    myListView2.setModel(myListModel)

    # 表示
    myListView1.show()
    myListView2.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()