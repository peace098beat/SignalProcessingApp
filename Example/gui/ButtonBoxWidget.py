# -*- coding: utf-8 -*-
u"""ButtonBoxWidget
"""
import sys
from PyQt4 import QtGui, QtCore

# PyQt4 imports
# PyQt OpenGL
# PyOpenGL imports


class ButtonBoxWidget(QtGui.QWidget):

    """ボタンボックスウィジェット
    """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.setup_ui()

    def setup_ui(self):
        # ボタンウィジェットの生成
        self.start_button = QtGui.QPushButton("Play", parent=self)
        self.load_button = QtGui.QPushButton("LOAD", parent=self)
        self.plot_button = QtGui.QPushButton("PLOT", parent=self)
        self.analys_button = QtGui.QPushButton("ANALYS", parent=self)
        # スライダーウィジェットの生成
        self.slider_low = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider_high = QtGui.QSlider(QtCore.Qt.Horizontal)

        # ボタンウィジェットをレイアウトに追加
        widget_button = QtGui.QWidget()
        layout_button = QtGui.QHBoxLayout()
        layout_button.addStretch(1)
        widget_button.setLayout(layout_button)
        layout_button.addWidget(self.start_button)
        layout_button.addWidget(self.load_button)
        layout_button.addWidget(self.plot_button)
        layout_button.addWidget(self.analys_button)

        # スライダーウィジェットのレイアウト
        widget_slider = QtGui.QWidget()
        layout_slider = QtGui.QHBoxLayout()
        layout_slider.addStretch(1)
        widget_slider.setLayout(layout_slider)
        layout_slider.addWidget(self.slider_low)
        layout_slider.addWidget(self.slider_high)

        layout = QtGui.QVBoxLayout()
        # layout.addStretch(1)
        layout.addWidget(widget_button)
        layout.addWidget(widget_slider)
        self.setLayout(layout)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setGeometry(100, 100, 600, 600)
    widget = ButtonBoxWidget()
    window.setCentralWidget(widget)

    window.show()
    app.exec_()

    dumy = 1
    dumy = 2
