# coding: utf-8
"""PyQtOpenGLSkel.py


Reference:
< http://www.not-enough.org/abe/manual/api-aa09/pyqt1.html >

"""
__author__ = "Tomoyuki Nohara <fififactory.com>"
__status__ = "production"
__version__ = "0.0.1"
__date__ = "2015.04.29"


#!env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *
import numpy as np


width = 400
height = 400
axrng = 7.


class GLPlotWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(300, 300)

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1., 1., 1.)
        glBegin(GL_LINES)
        glEnd()

        glBegin(GL_POINTS)
        # Plotting routines
        for x in np.arange(-axrng, axrng, 0.4):
            for y in np.arange(-axrng, axrng, 0.4):
                r = np.cos(x) + np.sin(y)
                glColor3f(np.cos(y * r), np.cos(x * y * r), np.sin(r * x))
                glVertex2f(x, y)
        glEnd()

        glFlush()

    def resizeGL(self, w, h):
        # ウィンドウサイズが0になるのを回避
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)

        # リサイズ後ウィンドウの位置・サイズ情報の再取得
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # ウィンドウの縦横比に対応して座標系を指定
        if w <= h:
            gluOrtho2D(-axrng, axrng, -axrng * h / w, axrng * h / w)
        else:
            gluOrtho2D(-axrng * w / h, axrng * w / h, -axrng, axrng)

        # 再設定後の位置・サイズ情報を更新
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        pass


class GLPlotWidget2(GLPlotWidget):

    """docstring for GLPlotWidget2"""

    def __init__(self, parent):
        super(GLPlotWidget2, self).__init__(parent)
        pass

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1., 1., 1.)
        glBegin(GL_LINES)
        glEnd()

        glBegin(GL_POINTS)
        # Plotting routines
        for x in np.arange(-axrng, axrng, 0.2):
            for y in np.arange(-axrng, axrng, 0.4):
                r = np.cos(x) + np.sin(y)
                glColor3f(np.cos(y * r), np.cos(x * y * r), np.sin(r * x))
                glVertex2f(x, y)
        glEnd()

        glFlush()


class QTGLSample(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        widget = GLPlotWidget2(self)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QTGLSample()
    window.setWindowTitle('PyQt OpenGL 1')
    window.show()
    sys.exit(app.exec_())

    dumy = 1
    dumy = 2
