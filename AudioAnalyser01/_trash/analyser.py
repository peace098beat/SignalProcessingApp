#! coding:utf-8
import sys
import wave
import time

import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PySide import QtGui, QtCore
import pylab as pl

import numpy as np



def wavread(filename):
    # Load Audio
    wf = wave.open(filename, "r")
    fs = wf.getframerate()
    x = wf.readframes(wf.getnframes())
    bit = wf.getsampwidth()
    amp = (2 ** 8) ** bit / 2.
    x = np.frombuffer(x, dtype="int16") / amp
    wf.close()
    return x, float(fs)

class Struct(object):
    ''' 解析結果格納用クラス(疑似構造体)
    '''
    def __init__(self, **kargs):
        for key, val in kargs.iteritems():
            setattr(self,key,val)

        self.wav = None
        self.fs = None
        self.framesize = None
        self.startframe = None
        self.maxframe = None
        self.nframe = None
        self.wavdata = None
        self.trange = None
        self.dft = None
        self.Adft = None
        self.Pdft = None
        self.fscale = None
        self.fscalek = None
        self.AdftLog = None
        self.cps = None
        self.quefrency = None
        self.cepCoef_env = None
        self.cpsLif_env = None
        self.dftSpc_env = None
        self.cepCoef_det = None
        self.cpsLif_det = None
        self.dftSpc_det = None


def analyser():

    print 'analyser start..'
    starttime = time.time()

    # 解析結果
    Metricdata = Struct()

    wav, fs = wavread("golf_D.wav")
    t = np.arange(0.0, len(wav) / fs, 1 / fs)

    Metricdata.wav = wav
    Metricdata.fs = fs
    Metricdata.framesize = 1024 * 1
    Metricdata.startframe = 1
    Metricdata.maxframe = len(Metricdata.wav) / Metricdata.framesize
    Metricdata.nframe = 5

    MS = 1000
    framesize = Metricdata.framesize
    startframe = Metricdata.startframe
    maxframe = Metricdata.maxframe
    nframe = Metricdata.nframe  # nframe = {1, 2, 3,..., maxframe}

    print 'maxframe', maxframe

    ss = (nframe - 1) * framesize
    se = nframe * framesize - 1

    wavdata = wav[ss:se]
    trange = t[ss:se] * MS

    # hanning window
    # hanningWindow = np.hanning(len(wavdata))
    # wavdata = wavdata * hanningWindow

    Metricdata.wavdata = wavdata
    Metricdata.trange = trange

    # fourier
    dft = np.fft.fft(wavdata, framesize)
    Adft = np.abs(dft)
    Pdft = Adft ** 2
    fscale = np.fft.fftfreq(framesize, d=1.0 / fs)
    fscalek = fscale / 1000

    Metricdata.dft = dft
    Metricdata.Adft = Adft
    Metricdata.Pdft = Pdft
    Metricdata.fscale = fscale
    Metricdata.fscalek = fscalek

    # cepstrum
    AdftLog = 20 * np.log10(Adft)
    cps = np.real(np.fft.ifft(AdftLog))
    quefrency = np.arange(0, len(cps))

    Metricdata.AdftLog = AdftLog
    Metricdata.cps = cps
    Metricdata.quefrency = quefrency

    # liftering
    # エンベロープenvlope
    cepCoef_env = 30
    cpsLif = np.array(cps)
    cpsLif[cepCoef_env:len(cpsLif) - cepCoef_env + 1] = 0
    dftSpc_env = np.fft.fft(cpsLif, framesize)
    dftSpc_env = np.real(dftSpc_env)

    Metricdata.cepCoef_env = cepCoef_env
    Metricdata.cpsLif_env = cpsLif
    Metricdata.dftSpc_env = dftSpc_env


    # 微細成分 detail
    cepCoef_det = cepCoef_env
    cpsLif = np.array(cps)
    cpsLif[0:cepCoef_det-1] = 0
    cpsLif[len(cpsLif) - cepCoef_det + 1:-1] = 0
    dftSpc_det = np.fft.fft(cpsLif, framesize)
    dftSpc_det = np.real(dftSpc_det)

    Metricdata.cepCoef_det = cepCoef_det
    Metricdata.cpsLif_det = cpsLif
    Metricdata.dftSpc_det = dftSpc_det

    print 'Analyser() Fin ...'
    print "Analysis_time:%0.1fms" % ((time.time()-starttime)*1000)
    return Metricdata


if __name__ == "__main__":

    # アナライズ
    Metricdata = analyser()

    # Create Qt Application
    app = QtGui.QApplication([])

    # Create Figure Object
    fig = pl.Figure(figsize=(100,100), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))

    ax1 = fig.add_subplot(3,2,1)
    ax1.plot(Metricdata.trange, Metricdata.wavdata )

    ax2 = fig.add_subplot(3,2,2)
    ax2.plot(Metricdata.fscalek, Metricdata.AdftLog)

    ax3 = fig.add_subplot(3,2,3)
    ax3.plot(Metricdata.fscalek, Metricdata.dftSpc_env)

    ax4 = fig.add_subplot(3,2,4)
    ax4.plot(Metricdata.fscalek, Metricdata.dftSpc_det)
    pl.xlim(0, 2)

    ax5 = fig.add_subplot(3,2,5)

    # MatplotオブジェクトをPySide用Widgetに変換
    canvas = FigureCanvas(fig)

    # butoon
    # plot_button = QtGui.QPushButton("plot")
    # play_button = QtGui.QPushButton("play")
    #
    # slider1 = QtGui.QSlider(QtCore.Qt.Horizontal)
    # slider2 = QtGui.QSlider(QtCore.Qt.Horizontal)
    # slider3 = QtGui.QSlider(QtCore.Qt.Horizontal)
    # slider4 = QtGui.QSlider(QtCore.Qt.Horizontal)

    # set layout
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    layout.addStretch(1)
    widget.setLayout(layout)
    # layout.addWidget(plot_button)
    # layout.addWidget(play_button)
    # layout.addWidget(slider1)
    # layout.addWidget(slider2)
    # layout.addWidget(slider3)
    # layout.addWidget(slider4)
    layout.addWidget(canvas)

    # Main Window Object
    win = QtGui.QMainWindow()
    win.setCentralWidget(widget)

    def on_plot():
        print 'on_plot'
    def on_play():
        print 'on_plot'


    # set SIGNAL
    # plot_button.clicked.connect(on_plot)
    # play_button.clicked.connect(on_play)

    # set SIGNAL Slider
    # slider1.valueChanged.connect()
    # slider2.valueChanged.connect()
    # slider3.valueChanged.connect()
    # slider4.valueChanged.connect()


    # show
    win.show()
    sys.exit(app.exec_())