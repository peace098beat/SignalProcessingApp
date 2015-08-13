# -*- coding: utf-8 -*-
"""GLPlotWidget グラフ描画ウィジェット
このクラスはOpenGLを使い、セットされた配列を描画するクラスです。

Property:
    width:  デフォルト画面サイズ
    height: デフォルト画面サイズ
    data:   グラフプロットの元データ

Method:
    set_data(arg_data): 描画元データの指定
        @arg_data:  2次元配列(-1<x<1, -1<y<1)

Example:
    app = QtGui.QApplication()
    window = QtGui.QMainWindow()
    widget = QLPlotWidget()
    widget.set_data(plot_data)
    window.setCentralWidget(widget)
    window.show()
    app.exec_()

Reference:
    < http://www.not-enough.org/abe/manual/api-aa09/pyqt1.html >

..Todo: 二次元波形描画機能
..Todo: イメージコンター描画機能
"""
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
from hsv2rgb import *

__author__ = "Tomoyuki Nohara <fififactory.com>"
__status__ = "production"
__version__ = "0.0.1"
__date__ = "2015.04.29"


class GLPlotWidget(QGLWidget):

    width = 400
    height = 400
    axrng = 1.

    def __init__(self, parent=None, data=None):
        QGLWidget.__init__(self, parent)
        # self.set_data(np.sin(2 * np.pi * 2 * np.linspace(-1, 1, 100)))
        # self.paint()
        self.initializeGL()
        self.data = np.zeros(0)
        self.count = 0

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def set_data(self, data):
        self.data = data

    def paintGL(self):
        """ OpenGLメソッド
        継承用にpaint()メソッドを呼び出す
        """
        self.paint()
        # if self.count == 0:
        # self.paint()
        # self.count = self.count + 1
        pass

    def paint(self):
        print '== paint:: =='
        pass

    def resizeGL(self, w, h):
        # ウィンドウサイズが0になるのを回避
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)

        FIX_ASPCT = 0

        if FIX_ASPCT:
            # リサイズ後ウィンドウの位置・サイズ情報の再取得
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()

            # ウィンドウの縦横比に対応して座標系を指定
            if w <= h:
                gluOrtho2D(-self.axrng, self.axrng, -self.axrng * h / w, self.axrng * h / w)
            else:
                gluOrtho2D(-self.axrng * w / h, self.axrng * w / h, -self.axrng, self.axrng)

            # 再設定後の位置・サイズ情報を更新
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()


class GLWavePlot(GLPlotWidget):

    def __init__(self, parent=None, data=None):
        GLPlotWidget.__init__(self, parent)
        self.data = np.zeros(0)
        # self.set_data(np.sin(2 * np.pi * 2 * np.linspace(-1, 1, 100)))

    # def set_data(self, data):
    #     self.data = data

    def paint(self):

        if np.all(self.data == 0):
            return 0

        print '== waveplot::paint:: =='

        # 描画の初期化
        # -----------
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # プロット色を選択
        # ---------------
        glColor3f(1., 0., 1.)

        # 線の種類を選択
        # -------------
        # glBegin(GL_LINES)
        glBegin(GL_LINE_STRIP)
        # glBegin(GL_POINTS)

        skip = 2
        gdata = self.data[::skip]

        if gdata.ndim == 1:
            """ シグナルプロット(横データなし)"""
            # プロット数
            N = gdata.shape[0]
            # 横軸の作成
            t = np.linspace(-1. * self.axrng, self.axrng, N)
            for i in range(0, N):
                x = t[i]
                y = gdata[i]
                glVertex2f(x, y)

        elif gdata.ndim == 2:
            # 配列を列行列に変換
            if gdata.shape[0] < gdata.shape[1]:
                gdata = gdata.T
            else:
                gdata = gdata

            # if gdata.shape[1] == 2:
            # """ シグナルプロット """
            N = gdata.shape[0]
            for i in range(0, N):
                x = gdata[i, 0]
                y = gdata[i, 1]
                glVertex2f(x, y)

        glEnd()
        glFlush()


class GLImagePlot(GLPlotWidget):

    """
    2次元コンターの描画用クラス

    Parameters
    ----------
    data: グラフにプロットするデータ.
        1-D(N,) or 2-D(N,2)配列のみ利用可能


    Attributes
    ----------

    Method
    ------
    set_data: 描画用のデータを整形し格納

    Notes
    -----

    """

    # 実際に描画する画素数
    pix_width = 600
    pix_height = 200
    axrng = 1.

    def __init__(self, parent=None, data=None):
        GLPlotWidget.__init__(self, parent)
        # self.set_data(np.random.randn(50, 50))
        # self.set_data(np.random.randn(500, 500))
        # self.paint()
        self.rang_l = 0.0
        self.rang_h = 1.0

    def set_data(self, data):
        print '== set_data =='
        self.data = data

        gdata = self.data
        if self.data.ndim == 1:
            """ シグナルプロット(横データなし)"""
            print "WARNING: Dimension is empty :", self.data.ndim
            return 0

        elif gdata.ndim == 2:
            # 配列を列行列に変換
            if gdata.shape[0] < gdata.shape[1]:
                gdata = gdata.T
            else:
                gdata = gdata

            if gdata.shape[1] == 2:
                """ シグナルプロット """
                print "WARNING: Dimension is empty :", gdata.ndim
                return 0

        print 'gdata.shpae', gdata.shape

        # 元データのサイズ
        N = gdata.shape[0]
        M = gdata.shape[1]
        # 描画する画素数
        N_lim = self.pix_width
        M_lim = self.pix_height
        # ステップ数の算出(繰り上げ計算)
        N_step = np.ceil(1. * N / N_lim)
        M_step = np.ceil(1. * M / M_lim)
        # 元データの削減
        C = gdata[::N_step, ::M_step]
        # C_MIN = C.min()
        # C = (C - C_MIN)
        # C_MAX = C.max()
        # C = C / C_MAX
        C_MAX = C.max()
        # 実際の描画数
        N_num = C.shape[0]
        M_num = C.shape[1]

        # プロット用の座標を定義
        # --------------------
        X = np.linspace(-1. * self.axrng, self.axrng, N_num)
        Y = np.linspace(-1. * self.axrng, self.axrng, M_num)

        # メンバ変数に格納
        # ---------------
        self.X = X
        self.Y = Y
        self.C = C
        self.C_MAX = C_MAX
        # プロット用の色配列を定義
        # ----------------------

        # C_rgb = {}
        # for i in range(0, C.shape[0]):
        #     for j in range(0, C.shape[1]):
        #         c = C[i, j]
        # hsv系からrgbへ変換(0-1 >> 0-240.)
        #         h = 240. - (c / C_MAX * 240.)
        #         rgb = hsv2rgb(H=h)
        #         C_rgb[i, j] = rgb
        self.chg_crange()

    def chg_crange(self, rang_l=None, rang_h=None):
        if rang_l == None:
            rang_l = self.rang_l
        if rang_h == None:
            rang_h = self.rang_h

        print 'rang_l=', rang_l, ' rang_h=', rang_h
        C_rgb = {}
        C_ary = self.C
        for i in range(0, C_ary.shape[0]):
            for j in range(0, C_ary.shape[1]):
                c = C_ary[i, j] / self.C_MAX
                # hsv系からrgbへ変換(0-1 >> 0-240.)
                A = (240. - 0.) / (rang_h - rang_l)
                B = -1. * A * rang_l
                h = A * c + B

                if h>240.:
                    h = 240.
                if h<0.:
                    h = 0.

                h_inv = 240. - h
                rgb = hsv2rgb(H=h_inv)
                C_rgb[i, j] = rgb

        self.C_rgb = C_rgb
        # self.paint()
        # return C_rgb

    def paint(self):

        if np.all(self.data == 0):
            return 0

        """描画メソッド
        self.C_rgb配列のRGBデータを
        self.X, self.Yに従って描画する"""

        print '== paint:: =='
        # 一次元データの場合はプロットしない
        if self.data.ndim == 1:
            print 'WORNING: dimension'
            return 0

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # グラフ描画メソッド
        # ----------------

        print "-----------------------------"
        print "- paintGL::イメージプロット中 -"
        import time
        start = time.time()
        print "..."

        glPointSize(4.0)
        glBegin(GL_POINTS)
        for i in range(0, self.C.shape[0]):
            for j in range(0, self.C.shape[1]):
                # 色データの指定
                glColor3f(self.C_rgb[i, j][0], self.C_rgb[i, j][1], self.C_rgb[i, j][2])
                # 頂点データの指定
                glVertex2f(self.X[i], self.Y[j])
        glEnd()

        print("elapsed_time:{0}".format(time.time() - start))
        print "- paintGL::イメージプロット終了 -"
        print "--------------------------------"

        # 座標軸の表示
        # -----------
        glBegin(GL_LINES)
        # glVertex2f(-1. * self.axrng, -1. * self.axrng)
        # glVertex2f(self.axrng, self.axrng)
        # glVertex2f(-1. * self.axrng, self.axrng)
        # glVertex2f(self.axrng, -1. * self.axrng)
        glEnd()

        glFlush()


class QTGLSample(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # widget = GLPlotWidget(self)
        # widget = GLWavePlot(self)
        widget = GLImagePlot(self)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QTGLSample()
    window.setWindowTitle('PyQt OpenGL 1')
    window.show()
    sys.exit(app.exec_())
    hsv2rgb(h, s, v)

    dumy = 1
    dumy = 2
2
2

2
