#! coding:utf-8
"""
gui_SignalLoadWidget

オーディオファイル(.wav)をロードし、
信号波形を表示するアプリケーション
"""
__appname__ = "gui_SignalLoadWidget"

import sys
import wave
import time

import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PySide.QtCore import *
from PySide.QtGui import *

# import pylab as pl
import matplotlib.pyplot as plt
import numpy as np

# ユーザーファンクション
from gui_FileLoadWidget import SimpleFileLoader
from gui_MasterOfMainWindow import MasterOfMainWindow
from FiSig.audiolab import wavread
from FiSig.stft import stft

from FiSig.axisLimitSelector import AxisLimitSelector3D, AxisLimitSelector2D, AxisLimitSelector


##########################################################
# Example
##########################################################
class ExampleMainWindow(MasterOfMainWindow):
    def __init__(self):
        MasterOfMainWindow.__init__(self)
        self.setWindowTitle(__appname__)
        self.setGeometry(300, 250, 400, 300)
        # スタイルシート
        # ----------------------------------------------------- #
        # self.setStyleSheet("background-color:white;")
        # 背景を白にする
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # GUI初期セットアップ関数
        # ----------------------------------------------------- #
        self.setupUI()
        self.setupEvent()

    ###############################################
    # UIを作成する関数
    ###############################################
    def setupUI(self):
        ###################################
        # MainWindowのセントラルウィジェット(panel)の生成
        # MainWindow直下のレイアウトを生成
        ###################################
        self.panel = QWidget()
        self.mainlayout = QVBoxLayout(self.panel)
        self.setCentralWidget(self.panel)

        ###################################
        # メインレイアウトにfileloaderを設置
        ###################################
        self.file_loader = SimpleFileLoader()
        self.mainlayout.addWidget(self.file_loader)

        ###################################
        # メインレイアウトにグラフプロットボタンを設置
        ###################################
        # btn_plot = QPushButton("plot")
        # self.mainlayout.addWidget(btn_plot)

        ###################################
        # 波形描画グラフを設置
        ###################################
        # Figure 1
        self.fig1 = plt.figure(figsize=(1, 1), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax1 = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.ax1_sub = plt.subplot2grid((1, 10), (0, 9))

        self.canvas1 = FigureCanvas(self.fig1)
        self.mainlayout.addWidget(self.canvas1)

        ###################################
        # STFTグラフを設置
        ###################################
        # Figure 2
        self.fig2 = plt.figure(figsize=(1, 1), dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax2 = plt.subplot2grid((1, 10), (0, 0), colspan=9)
        self.ax2_sub = plt.subplot2grid((1, 10), (0, 9))

        self.canvas2 = FigureCanvas(self.fig2)
        self.mainlayout.addWidget(self.canvas2)

        ###################################
        # GWTグラフを設置
        ###################################
        # Figure 3
        self.selector3 = AxisLimitSelector()
        self.fig3, self.ax3, self.ax3_sub = self.selector3.getHandle()
        self.canvas3 = FigureCanvas(self.fig3)
        self.mainlayout.addWidget(self.canvas3)

    ###############################################
    # イベントを設定する関数
    ###############################################
    def setupEvent(self):
        self.file_loader.fileloaded.connect(self.fileload)

    @Slot()
    def fileload(self):
        print 'File Load..'
        self.wavfilepath = self.file_loader.abspath
        self.statusBar().showMessage("File Loaded..%s" % (str(self.wavfilepath)), 5000)
        print str(self.wavfilepath)

        self.analysis()

    def analysis(self):

        [data, fs] = wavread(self.wavfilepath)
        data = data[0:fs - 1]
        N = len(data)

        fontsize = 10

        # *****************************
        # オーディオファイルのプロット
        # *****************************
        self.ax1.cla()
        self.ax1.plot(data)
        ls1 = AxisLimitSelector2D(data, self.fig1, self.ax1, self.ax1_sub)

        # self.fig1.tight_layout()
        self.ax1.set_xlabel('Time [s]', fontsize=fontsize)
        self.ax1.set_ylabel('Amplitude [-]]', fontsize=fontsize)
        self.ax1.locator_params(nbins=10, axis='x', tight=None)
        self.ax1.locator_params(nbins=3, axis='y', tight=None)
        self.canvas1.draw()

        # *****************************
        # STFT
        # *****************************
        from scipy import hanning
        fftLen = 512
        win = hanning(fftLen)
        step = fftLen / 2
        spectrogram = abs(stft(data, win, step)[:, : fftLen / 2 + 1]).T
        spectrogram = 20 * np.log10(spectrogram)
        self.ax2.cla()
        self.ax2.imshow(spectrogram, origin="lower", aspect="auto", cmap="jet")
        ls2 = AxisLimitSelector3D(spectrogram, self.fig2, self.ax2, self.ax2_sub)
        # self.fig2.tight_layout()
        self.ax2.set_xlabel('Time [s]', fontsize=fontsize)
        self.ax2.set_ylabel('Frequency [Hz]', fontsize=fontsize)
        self.ax2.locator_params(nbins=10, axis='x', tight=None)
        self.ax2.locator_params(nbins=3, axis='y', tight=None)
        self.canvas2.draw()

        # *****************************
        # GWT
        # *****************************
        from FiSig.gwt import gwt
        import time

        self.statusBar().showMessage("GWT running ..", 5000)

        # 時間計測開始
        start = time.time()
        # GWT解析を実行する
        d_gwt, trange, frange = gwt(data, Fs=fs)

        # 解析終了と、解析時間を表示する
        self.statusBar().showMessage("GWT fin ... analys time %0.2f[s]" % (time.time() - start), 10000)

        d_gwt = 20 * np.log10(np.abs(d_gwt))
        extent = trange[0], trange[-1], frange[0], frange[-1]
        gdata = d_gwt[::10, ::10]

        self.ax3.cla()
        im = self.ax3.imshow(np.flipud(gdata.T), cmap='jet', extent=extent)
        self.selector3.setData(d_gwt, "3D")

        self.ax3.axis('auto')
        self.ax3.set_title('Scarogram (GWT)', fontsize=fontsize)
        self.ax3.title.set_visible(False)
        self.ax3.set_xlabel('Time [s]', fontsize=fontsize)
        self.ax3.set_ylabel('Frequency [Hz]', fontsize=fontsize)
        self.ax3.locator_params(nbins=10, axis='x', tight=None)
        self.ax3.locator_params(nbins=3, axis='y', tight=None)
        self.canvas3.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ExampleMainWindow()
    w.show()
    sys.exit(app.exec_())
