#! coding:utf-8
"""
ファイルシステムをリスト表示するオブジェクト


"""
import sys
from PySide import QtCore, QtGui

def main():
    app = QtGui.QApplication(sys.argv)


    currentpath = QtCore.QDir.currentPath()

    rootpath = ''


    model = QtGui.QFileSystemModel()
    model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
    model.setRootPath('')

    tree = QtGui.QTreeView()
    tree.setRootIndex(model.index(rootpath))
    tree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
    tree.setModel(model)
    tree.setCurrentIndex(model.index(currentpath))
    tree.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()