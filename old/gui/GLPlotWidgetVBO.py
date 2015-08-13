# -*- coding: utf-8 -*-
"""GLPlotWidget グラフ描画ウィジェット
このクラスはOpenGLを使い、セットされた配列を描画するクラスです。
描画にはOpenGL.arrays.vbo.VOBを用いています。
二次元波形表示、コンター表示等は未実装です。
OpenGLの動作確認用の目的です。

Property:
    width:  デフォルト画面サイズ
    height: デフォルト画面サイズ
    data:   グラフプロットの元データ
    count:  プロット点数
    vob:    OpenGL頂点用バッファ

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

..Todo: 二次元波形描画機能
..Todo: イメージコンター描画機能
"""
import sys

import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
from PyQt4 import QtGui
from PyQt4.QtOpenGL import QGLWidget


class GLPlotWidget(QGLWidget):

    """OpenGL用のWidgetを作成
    """
    # default window size
    width, height = 600, 600

    def __init__(self):
        super(GLPlotWidget, self).__init__()

    def set_data(self, data):
        # クラスプロパティに追加
        self.data = data
        self.count = self.data.shape[0]
        self.__initializeGL()
        self.updateGL()

    def __initializeGL(self):
        u"""Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # bacground Color
        gl.glClearColor(0, 0, 0, 0)
        # create a Vertex BUffer Object with the specified data
        self.vbo = glvbo.VBO(self.data)

    def paintGL(self):
        """paint the scene. (オーバーライド)
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set color for vertex
        gl.glColor(1, 1, 0)
        gl.glPointSize(0.1)
        """ bind the VBO """
        self.vbo.bind()
        # tell openGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        # these vertices contain 2 single precision coordinates
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vbo)
        # draw "count" points from the VBO
        gl.glDrawArrays(gl.GL_POINTS, 0, self.count)

    def resizeGL(self, width, height):
        """Called upon window resizing: reinitalize the viewport.(オーバーライド)
        """
        # update the window size
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are(-+1, -+1)
        gl.glOrtho(-1, 1, 1, -1, -1, 1)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setGeometry(100, 100, 600, 600)
    widget = GLPlotWidget()
    window.setCentralWidget(widget)

    window.show()
    app.exec_()

    damy = 1
    damy = 2
