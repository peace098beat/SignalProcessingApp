#! coding:utf-8
"""
BaseMplCanvas : matplotlibを使ったグラフウィジェット
GwtMplCanvas : ガボールウェーブレット表示用ウィジェット
"""
import sys

from PySide.QtGui import *
from PySide.QtCore import *

import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt


class BaseMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """

    def __init__(self, parent=None, width=5, height=4, dpi=72):
        # fiugrueの生成
        self.fig = Figure(figsize=(width, height), dpi=dpi,
                          facecolor=[0.5, 0.5, 0.5], edgecolor=None,
                          linewidth=1.0,
                          frameon=True, tight_layout=True)
        # axesハンドルの生成
        self.axes = self.fig.add_subplot(111)

        # 再描画では上書きしない
        self.axes.hold(False)

        # 画像の初期表示
        self.compute_initial_fiugre()

        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)

        # 親のウィジェットを生成
        self.setParent(parent)

        # サイズの設定
        # FigureCanvas.setSizePolicy(self,
        #                            QtGui.QSizePolicy.Expanding,
        #                            QtGui.QSizePolicy.Expanding)

        # サイズの更新
        FigureCanvas.updateGeometry(self)

    def compute_initial_fiugre(self):
        """グラフの軸の設定項目を書く"""
        self.axes.plot([1], [1])
        pass

    def update_figure(self, xdata=None, ydata=None):
        self.draw()
        pass

    # def plot(self, xdata=None, ydata=None):
    #     pass