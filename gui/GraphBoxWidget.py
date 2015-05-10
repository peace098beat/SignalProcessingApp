# -*- coding: utf-8 -*-
"""GraphBoxWidget
GLPlotWidgetをレイアウトのためのクラス。
グラフ描画ウィジェットに描画データを渡すのが主な役割。

Property:
    am:
    data:
    glwidget1:
    glwidget2:
    layout;

Method:
    replot_graph(): 子オブジェクトの再描画


"""
import sys
import numpy as np
import scipy
from PyQt4 import QtGui
from GLPlotWidget import *
from gaborwavelet import *


class WaveGraphWidget(GLWavePlot):

    """
    信号波形をグラフプロットするウィジェットクラス.

    Parameters
    ----------
    data: グラフにプロットするデータ.
        1-D(N,) or 2-D(N,2)配列のみ利用可能


    Attributes
    ----------
    ...

    Method
    ------
    calc: 描画用データを生成

    Notes
    -----
    描画用データ(data)と、入力データ(楽曲データ)は別なので注意。
    基本的に楽曲データは格納しない。
    グラフウィジェットなので、calc()は一度だけしか行われない。

    """

    def __init__(self, parent=None, data=None):
        GLWavePlot.__init__(self, parent)

    def calc(self, adata):
        self.set_data(adata)


class GWTGraphWidget(GLImagePlot):

    """
    ガボールウェーブレット変換結果をコンタープロットするウィジェットクラス.

    Parameters
    ----------
    data: グラフにプロットするデータ.
        2-D(N,M)配列のみ利用可能.

    Attributes
    ----------
    ...

    Method
    ------
    calc: 描画用データを生成

    Notes
    -----
    描画用データ(data)と、入力データ(楽曲データ)は別なので注意。
    基本的に楽曲データは格納しない。
    グラフウィジェットなので、calc()は一度だけしか行われない。

    """

    def __init__(self, parent=None):
        GLImagePlot.__init__(self, parent)

    def calc(self, adata, Fs):
        wt_data = GWTAnalysis(adata, Fs=Fs)
        pdata = np.abs(wt_data)
        # pdata = pdata / pdata.max()
        # pdata = 20 * np.log10(pdata)
        pdata = np.log(pdata)

        # 描画データの格納
        self.set_data(pdata)


class STFTGraphWidget(GLImagePlot):

    """
    STFT結果をコンタープロットするウィジェットクラス.

    Parameters
    ----------
    data: グラフにプロットするデータ.
        2-D(N,M)配列のみ利用可能.

    Attributes
    ----------
    ...

    Method
    ------
    calc: 描画用データを生成

    Notes
    -----
    描画用データ(data)と、入力データ(楽曲データ)は別なので注意。
    基本的に楽曲データは格納しない。
    グラフウィジェットなので、calc()は一度だけしか行われない。

    """

    def __init__(self, parent=None):
        GLImagePlot.__init__(self, parent)

    def calc(self, adata, Fs):
        anadata = self.stft(x=adata, fs=Fs, framesz=512, hop=10)
        pdata = np.abs(anadata)
        # pdata = pdata / pdata.max()
        # pdata = 20 * np.log10(pdata)
        pdata = np.log(pdata)

        # 描画データの格納
        self.set_data(pdata)

    def stft(self, x, fs, framesz, hop):
        # framesamp = int(framesz * fs)
        # hopsamp = int(hop * fs)
        framesamp = framesz
        hopsamp = hop
        w = scipy.hamming(framesamp)
        X = scipy.array([scipy.fft(w * x[i:i + framesamp])for i in range(0, len(x) - framesamp, hopsamp)])
        print X.shape
        X = X[:, :int(framesz / 2)]
        print "== fin stft =="
        return X


class GraphBoxWidget(QtGui.QWidget):

    """
    グラフのサムネイル表示クラス.
    """

    def __init__(self, parent=None, audiomanager=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.am = audiomanager
        self.__setup_ui()

    def __setup_ui(self):
        self.data = np.array(.2 * np.random.randn(100000, 2), dtype=np.float32)

        '- glwidget1(GLPlotWidget)'
        self.glwidget1 = WaveGraphWidget()
        self.glwidget1.calc(self.am.data_n)

        '- glwidget2(GLPlotWidget)'
        self.glwidget2 = GWTGraphWidget()
        self.glwidget2.calc(self.am.data_n, self.am.fs)

        '- glwidget3(GLPlotWidget)'
        self.glwidget3 = STFTGraphWidget()
        self.glwidget3.calc(self.am.data_n, self.am.fs)

        '- graph_box_widget(Qwidget)'
        self.setLayout(QtGui.QVBoxLayout())

        '* graph_layout(QHBoxLayout)'
        self.layout().addWidget(self.glwidget1)
        self.layout().addWidget(self.glwidget2)
        self.layout().addWidget(self.glwidget3)

    def replot_graph(self):
        """メイン処理部から再プロットが呼び出されたときの処理
        子オブジェクトのQLPlotWidgetの再描画メソッドを呼び出す
        """
        print "== replot_graph() =="
        # anadata = self.am.data_n[20000:70000]
        anadata = self.am.data_n
        self.glwidget1.calc(anadata)
        self.glwidget2.calc(anadata, self.am.fs)
        self.glwidget3.calc(anadata, self.am.fs)

    def chg_range_l(self, value):
        value = value / 100. / 2
        print ': Slider Value (Low)=', value
        self.glwidget2.rang_l = value
        self.glwidget3.rang_l = value

    def chg_range_h(self, value):
        value = value / 100. / 2 + 0.5
        print ': Slider Value (Low)=', value
        self.glwidget2.rang_h = value
        self.glwidget3.rang_h = value

    def plot(self):
        self.glwidget2.chg_crange()
        self.glwidget3.chg_crange()

        self.glwidget1.paintGL()
        self.glwidget2.paintGL()
        self.glwidget3.paintGL()


if __name__ == '__main__':

    from AudioManager import *
    # am = AudioManager(filepath='./audio/0321.wav')
    am = AudioManager(filepath='./audio/golf_D.wav')

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setGeometry(0, 0, 600, 600)
    widget = GraphBoxWidget(audiomanager=am)
    # widget.replot_graph()
    window.setCentralWidget(widget)

    window.show()
    app.exec_()

    dumy = 1
