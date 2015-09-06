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


###################################################
#
# Base
#
###################################################
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


###################################################
#
# wave
#
###################################################

class WaveMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """

    def __init__(self, parent=None, width=1, height=1, dpi=72):
        self.fontsize = 10
        # fiugrueの生成
        self.fig = plt.figure(figsize=(width, height), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0),
                              tight_layout=False)
        # self.fig = plt.figure(facecolor=(0.5, 0.5, 0.5), edgecolor=(0, 0, 0), tight_layout=False)
        # axesハンドルの生成
        self.axes = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.axes_sub = plt.subplot2grid((1, 10), (0, 9))
        # 再描画では上書きしない
        self.axes.hold(False)
        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)
        # 親のウィジェットを生成
        self.setParent(parent)
        # サイズの更新
        FigureCanvas.updateGeometry(self)

        # seakbarのハンドル
        self.seakbar_handle = None

        # 画像の初期表示
        self.compute_initial_fiugre()

    def compute_initial_fiugre(self):
        """グラフの軸の設定項目を書く"""
        self.axes.plot([1], [1])
        self.seakbar_handle = self.axes.plot([1], [1])
        # 目盛の設定
        self.axes_sub.set_xticklabels([])
        self.axes_sub.set_yticklabels([])
        pass

    def update_figure(self, xdata=None, ydata=None):
        self.draw()
        pass

    def plot(self, xdata=None, ydata=None):
        self.xdata = xdata
        self.ydata = ydata
        self.axes.plot(xdata, ydata)
        AxisLimitSelector2D(ydata, self.fig, self.axes, self.axes_sub)
        self.axes.set_xlabel('Time [s]', fontsize=self.fontsize)
        self.axes.set_ylabel('Amplitude [-]]', fontsize=self.fontsize)
        self.axes.locator_params(nbins=10, axis='x', tight=True)
        self.axes.locator_params(nbins=3, axis='y', tight=True)
        self.axes.axis('tight')
        self.axes.axis('auto')
        self.draw()

        self.axes.hold(True)
        self.seakbar_handle, = self.axes.plot([0], [0])
        self.axes.hold(False)
        pass

    @Slot()
    def updateAtTime(self, atTime):
        atTime_ratio = atTime / 100.

        t = atTime_ratio * self.xdata[-1]
        # self.axes.plot([t,t],[0,4000])
        self.seakbar_handle.set_xdata([t,t])
        self.seakbar_handle.set_ydata(self.axes.get_ylim())

        # -- 再描画 --
        self.draw()
        pass

###################################################
#
# GWT
#
###################################################

class GwtMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """

    def __init__(self, parent=None, width=5, height=4, dpi=72):
        self.fontsize = 10

        # fiugrueの生成
        self.fig = plt.figure(figsize=(width, height), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0),
                              tight_layout=False)
        # self.fig = plt.figure(facecolor=(0.5, 0.5, 0.5), edgecolor=(0, 0, 0), tight_layout=False)
        # axesハンドルの生成
        self.axes = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.axes_sub = plt.subplot2grid((1, 10), (0, 9))
        # 再描画では上書きしない
        self.axes.hold(False)
        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)
        # 親のウィジェットを生成
        self.setParent(parent)
        # サイズの更新
        FigureCanvas.updateGeometry(self)
        #
        self.seakbar_handle = None
        # 画像の初期表示
        self.compute_initial_fiugre()

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
        self.extent = extent
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

        self.axes.hold(True)
        self.seakbar_handle, = self.axes.plot([0], [0])
        self.axes.hold(False)
        pass

    @Slot()
    def updateAtTime(self, atTime):
        atTime_ratio = atTime / 100.

        t = atTime_ratio * self.extent[1]
        # self.axes.plot([t,t],[0,4000])
        self.seakbar_handle.set_xdata([t,t])
        self.seakbar_handle.set_ydata(self.axes.get_ylim())

        # -- 再描画 --
        self.draw()
        pass


###################################################
#
# SpectrumAtTimeMplCanvas
#
###################################################

class SpectrumAtTimeMplCanvas(FigureCanvas):
    """ FigureCanvasウィジェット
    """

    def __init__(self, parent=None, width=5, height=5, dpi=72):
        self.fontsize = 10
        # fiugrueの生成
        self.fig = plt.figure(figsize=(width, height), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0),
                              tight_layout=False)
        # axesハンドルの生成
        self.axes = self.fig.add_subplot(111)
        # 再描画では上書きしない
        self.axes.hold(False)
        # コンストラクタ
        FigureCanvas.__init__(self, self.fig)
        # 親のウィジェットを生成
        self.setParent(parent)
        # サイズの更新
        FigureCanvas.updateGeometry(self)

        # シークバーの格納
        self.seakbar_handle = None
        self.seakbar_xdata = [1, 1]
        self.seakbar_ydata = [-1, 1]

        # メインラインハンドルの格納
        self.mainline_handle = None

        # 画像の初期表示
        self.compute_initial_fiugre()

    def compute_initial_fiugre(self):
        """グラフの軸の設定項目を書く"""

        self.axes.hold(True)
        self.mainline_handle, = self.axes.plot([0, 2], [0, 2])
        # シークバーの準備
        self.seakbar_handle, = self.axes.plot(self.seakbar_xdata, self.seakbar_ydata)
        # 軸の設定
        self.axes.hold(False)

    def plot(self, atTime, zdata, trange, frange):
        # データの格納
        self.plot_data = zdata
        self.plot_frange = frange
        self.plot_trange = trange

        fdata = zdata[0, :]
        print 'fdata', fdata.size
        print 'trange', trange.size
        print 'frange', frange.size
        self.axes.plot(frange, fdata)
        pass

        # def plot(self, xdata=None, ydata=None):
        #     self.axes.hold(False)

        # self.line_of_main, = self.axes.plot(ydata)
        # self.mainline_handle.set_xdata = xdata
        # self.mainline_handle.set_ydata = ydata

        # -- 軸の設定 --
        # self.axes.set_title('SpectrumAtTimeMplCanvas')
        # self.axes.set_xlabel('Time [s]', fontsize=self.fontsize)
        # self.axes.set_ylabel('Amplitude [-]]', fontsize=self.fontsize)
        # self.axes.locator_params(nbins=10, axis='x', tight=True)
        # self.axes.locator_params(nbins=3, axis='y', tight=True)
        # self.axes.axis('tight')
        # self.axes.axis('auto')

        self.draw()
        pass

    @Slot()
    def updateAtTime(self, atTime):
        atTime_ratio = atTime / 100.

        Nt = len(self.plot_trange)
        print 'Nt', Nt
        print 'Nt*atTime_ratio', Nt * atTime_ratio

        num = np.ceil(Nt * atTime_ratio)

        Pdata = self.plot_data[num, :]

        self.axes.plot(self.plot_frange, Pdata)

        # -- 再描画 --
        self.draw()
        pass


####################################################################
# Demo
####################################################################
class GUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # self.canvas = WaveMplCanvas()
        self.canvas = SpectrumAtTimeMplCanvas()

        xdata = np.array([0, 0.5, 1.0, 1.5])
        ydata = np.array([0, 0.5, 0, 0.5])
        # self.canvas.plot(xdata=xdata, ydata=ydata)
        self.canvas.updateAtTime(aTtime=0.5)

        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())
