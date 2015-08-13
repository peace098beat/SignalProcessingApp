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
# from FiSig.imshow_sox import imshow_sox

def imshow_sox(spectrogram, rm_low = 0.1, axes=None):
    from scipy import hanning, hamming, histogram, log10

    # max_value = spectrogram.max()
    ### amp to dbFS
    # db_spec = log10(spectrogram / float(max_value)) * 20
    db_spec = log10(spectrogram) * 20
    # ### カラーマップの上限と下限を計算
    # hist, bin_edges = histogram(db_spec.flatten(), bins = 1000, normed = True)
    # hist /= float(hist.sum())
    # pl.hist(hist)
    # pl.show()
    # S = 0
    # ii = 0
    # while S < rm_low:
    #     S += hist[ii]
    #     ii += 1
    # vmin = bin_edges[ii]
    # vmax = db_spec.max()
    # if vmin>vmax:
    #     vmin, vmax = vmax, vmin

    # axes.imshow(db_spec, origin = "lower", aspect = "auto", cmap = "hot", vmax = vmax, vmin = vmin)
    axes.imshow(db_spec, origin = "lower", aspect = "auto", cmap = "hot")

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
        self.mainlayout =  QVBoxLayout(self.panel)
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
        self.fig1 = plt.Figure(figsize=(1,1), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        # self.fig1.patch.set_alpha(0.)
        self.ax1 = self.fig1.add_subplot(1,1,1)
        self.canvas1 = FigureCanvas(self.fig1)
        self.mainlayout.addWidget(self.canvas1)

        ###################################
        # STFTグラフを設置
        ###################################
        # Figure 2
        self.fig2 = plt.Figure(figsize=(1,1), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        self.ax2 = self.fig2.add_subplot(1,1,1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.mainlayout.addWidget(self.canvas2)

        ###################################
        # GWTグラフを設置
        ###################################
        # Figure 2
        self.fig3 = plt.Figure(figsize=(1,1), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        self.ax3 = self.fig3.add_subplot(1,1,1)
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
        [data, fs]=wavread(self.wavfilepath)
        data = data[0:fs-1]
        N = len(data)
        trange = np.linspace(0,)

        fontsize = 10
        # *****************************
        # オーディオファイルのプロット
        # *****************************
        self.ax1.plot(data)
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
        fftLen = 1024
        win = hanning(fftLen)
        step = fftLen / 2
        spectrogram = abs(stft(data, win, step)[:, : fftLen / 2 + 1]).T
        imshow_sox(spectrogram, rm_low=0.1, axes=self.ax2)
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
        d_gwt, trange, frange = gwt(data, Fs=fs)
        d_gwt = 20*np.log10(np.abs(d_gwt))
        extent = trange[0], trange[-1], frange[0], frange[-1]
        im = self.ax3.imshow(np.flipud(d_gwt.T), cmap='jet', extent=extent)
        self.ax3.axis('auto')
        self.ax3.set_title('Scarogram (GWT)', fontsize=fontsize)
        self.ax3.title.set_visible(False)
        self.ax3.set_xlabel('Time [s]', fontsize=fontsize)
        self.ax3.set_ylabel('Frequency [Hz]', fontsize=fontsize)
        self.ax3.locator_params(nbins=10, axis='x', tight=None)
        self.ax3.locator_params(nbins=3, axis='y', tight=None)
        # self.fig3.tight_layout()
        # self.fig3.colorbar(im)
        self.canvas3.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ExampleMainWindow()
    w.show()
    sys.exit(app.exec_())


