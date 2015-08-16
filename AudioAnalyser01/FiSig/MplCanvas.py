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

## GUIモジュール
from axisLimitSelector import AxisLimitSelector3D, AxisLimitSelector2D, AxisLimitSelector



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
        # self.axes.plot([1], [1])
        pass

    def update_figure(self, xdata=None, ydata=None):
        self.draw()
        pass

    # def plot(self, xdata=None, ydata=None):
    #     pass


class WaveMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """
    def __init__(self, parent=None, width=1, height=1, dpi=72):

        self.fontsize = 10
        # fiugrueの生成
        self.fig = plt.figure(figsize=(width, height), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0), tight_layout=False)
        # axesハンドルの生成
        self.axes = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.axes_sub = plt.subplot2grid((1, 10), (0, 9))
        # 再描画では上書きしない
        self.axes.hold(False)
        # 画像の初期表示
        self.compute_initial_fiugre()
        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)
        # 親のウィジェットを生成
        self.setParent(parent)
        # サイズの更新
        FigureCanvas.updateGeometry(self)



    def compute_initial_fiugre(self):
        """グラフの軸の設定項目を書く"""
        self.axes.plot([1], [1])


        # 目盛の設定
        self.axes_sub.set_xticklabels([])
        self.axes_sub.set_yticklabels([])

        pass

    def update_figure(self, xdata=None, ydata=None):
        self.draw()
        pass

    def plot(self, xdata=None, ydata=None):
        self.axes.plot(ydata)
        AxisLimitSelector2D(ydata, self.fig, self.axes, self.axes_sub)
        self.axes.set_xlabel('Time [s]', fontsize=self.fontsize)
        self.axes.set_ylabel('Amplitude [-]]', fontsize=self.fontsize)
        self.axes.locator_params(nbins=10, axis='x', tight=True)
        self.axes.locator_params(nbins=3, axis='y', tight=True)
        self.axes.axis('tight')
        self.axes.axis('auto')
        self.draw()
        pass


class GwtMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """
    def __init__(self, parent=None, width=5, height=4, dpi=72):

        self.fontsize = 10

        # fiugrueの生成
        # self.fig = plt.figure(figsize=(width, height), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0), tight_layout=False)
        self.fig = plt.figure(facecolor=(0.5, 0.5, 0.5), edgecolor=(0, 0, 0), tight_layout=False)
        # axesハンドルの生成
        self.axes = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.axes_sub = plt.subplot2grid((1, 10), (0, 9))
        # 再描画では上書きしない
        self.axes.hold(False)
        # 画像の初期表示
        self.compute_initial_fiugre()
        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)
        # 親のウィジェットを生成
        self.setParent(parent)
        # サイズの更新
        FigureCanvas.updateGeometry(self)

    def compute_initial_fiugre(self):
        """グラフの軸の設定項目を書く"""
        # self.axes.plot([1], [1])
        # 目盛の設定
        self.axes_sub.set_xticklabels([])
        self.axes_sub.set_yticklabels([])
        pass

    def update_figure(self, xdata=None, ydata=None):
        self.draw()
        pass

    def plot(self, xdata=None, ydata=None, zdata=None, extent=None):
        self.axes.plot(ydata)
        self.axes.imshow(np.flipud(zdata.T), cmap='jet', extent=extent)
        # GWT
        AxisLimitSelector3D(zdata, self.fig, self.axes, self.axes_sub)
        self.axes.set_xlabel('Time [s]', fontsize=self.fontsize)
        self.axes.set_ylabel('Frequency [Hz]', fontsize=self.fontsize)

        self.axes.locator_params(nbins=10, axis='x', tight=True)
        self.axes.locator_params(nbins=3, axis='y', tight=True, fontsize=1)

        self.axes.axis('tight')
        self.axes.axis('auto')
        self.draw()
        pass

###################################################
#
# Demo
#
###################################################
class GUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.canvas = WaveMplCanvas()
        ydata = np.array([1,2,3,4])
        self.canvas.plot(ydata=ydata)

        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())
