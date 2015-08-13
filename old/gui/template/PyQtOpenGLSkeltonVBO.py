# -*- coding: utf-8 -*-
u""" GLPlotWidget

version: 0.1
グラフを描画するクラスは作れたが、再描画が実装できない。
updateGLで再描画できるはずだが、クラス間での呼び出しのためか不可。
再度シンプルサンプルで試す必要がある。
(解決) self.vboの更新を忘れていた。クラスプロパティのdataと、
OpenGLの描画用配列VBOの存在を忘れていた。


PyQtOpenGL-Skelton.py
this is graph plot class for PyOpenGL

2D graphics rendering tutorial with PyOpenGL
< http://cyrille.rossant.net/2d-graphics-rendering-tutorial-with-pyopengl/ >

"""
# PyQt4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
# PyQt OpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

import GLPlotWidget

def pyAudioPlay():
	print 'play pyAudio'
	import pyaudio
	# ストリームを開く
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	# チャンク単位でストリームに出力し音声を再生
	chunk = 1024
	# 先頭に戻す
	wf.rewind()
	data = wf.readframes(chunk)
	while data != '':
		stream.write(data)
		data = wf.readframes(chunk)
		
	# clean
	stream.close()
	p.terminate()
	print 'end pyaudio'




class GraphBoxWidget(QtGui.QWidget):
	"""グラフのサムネイル表示クラス
	"""
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.init_data()
		self.setup_ui()

	def init_data(self):
		import numpy as np
		self.data = np.array(.2 * np.random.randn(100000,2), dtype=np.float32)
		print self.data


	def setup_ui(self):
		'- glwidget1(GLPlotWidget)'
		self.glwidget1 = GLPlotWidget()
		self.glwidget1.set_data(self.data)            

		'- glwidget1(GLPlotWidget)'
		self.glwidget2 = GLPlotWidget()
		self.glwidget2.set_data(self.data)

		'- graph_box_widget(Qwidget)'
		self.setLayout(QtGui.QVBoxLayout())

		'* graph_layout(QHBoxLayout)'
		self.layout().addWidget(self.glwidget1)
		self.layout().addWidget(self.glwidget2)

	def replot_graph(self):
		"""メイン処理部から再プロットが呼び出されたときの処理
		子オブジェクトのQLPlotWidgetの再描画メソッドを呼び出す
		"""
		self.glwidget1.reset_data()
		self.glwidget2.reset_data()



class ButtonBoxWidget(QtGui.QWidget):
	"""ボタンボックスウィジェット
	"""
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent=parent)
		self.setup_ui()

	def setup_ui(self):
		self.start_button = QtGui.QPushButton("STRAT", parent=self)
		self.load_button = QtGui.QPushButton("LOAD", parent=self)
		self.plot_button = QtGui.QPushButton("PLOT", parent=self)
		self.analys_button = QtGui.QPushButton("ANALYS", parent=self)

		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.start_button)
		layout.addWidget(self.load_button)
		layout.addWidget(self.plot_button)
		layout.addWidget(self.analys_button)

		self.setLayout(layout)



if __name__ == '__main__':
	# import numpy for generating random data points
	import sys
	import numpy as np
	import wave

	# Global variable of Audio
	global audio_object
	audio_object = {
		'name': 'audio1.wav'
	}
	global wf
	wf = wave.open("./audio/golf_D.wav", "r")
	# buffer = wf.readframes(wf.getnframes())
	# pyAudioPlay()



	# define a Qt window with an OpenGL widget inside it
	class TestWindow(QtGui.QMainWindow):
		def __init__(self):
			super(TestWindow, self).__init__()
			# put the window at the screen position (100, 100)
			main_width = 600
			main_height = 600
			self.setGeometry(100, 100, main_width, main_height)
			
			# generate random data points
			self.data = np.array(.2 * np.random.randn(100000,2), dtype=np.float32)

			"""
			panel_widget(QWidget) -
				* panel_layout(QVBoxLayout)
				- graph_box_widget(Qwidget)
					* graph_layout(QHBoxLayout)
					- glwidget1(GLPlotWidget)
					- glwidget2(GLPlotWidget)
				- button_box_widget(ButtonBoxWidget)
			"""

			'panel_widget(QWidget)'
			self.panel_widget = QtGui.QWidget()
			self.panel_widget.setLayout(QtGui.QVBoxLayout())

			# '- glwidget1(GLPlotWidget)'
			# self.glwidget1 = GLPlotWidget()
			# self.glwidget1.set_data(self.data)            

			# '- glwidget1(GLPlotWidget)'
			# self.glwidget2 = GLPlotWidget()
			# self.glwidget2.set_data(self.data)

			# '- graph_box_widget(Qwidget)'
			# graph_box_widget = QtGui.QWidget()
			# graph_box_widget.setLayout(QtGui.QHBoxLayout())

			# '* graph_layout(QHBoxLayout)'
			# graph_box_widget.layout().addWidget(self.glwidget1)
			# graph_box_widget.layout().addWidget(self.glwidget2)

			button_box_widget = ButtonBoxWidget()
			graph_box_widget = GraphBoxWidget()

			'* panel_layout(QVBoxLayout)'
			self.panel_widget.layout().addWidget(graph_box_widget)
			self.panel_widget.layout().addWidget(button_box_widget)
			self.setCentralWidget(self.panel_widget)

			u'SIGNALの接続'
			button_box_widget.start_button.clicked.connect(pyAudioPlay)
			button_box_widget.load_button.clicked.connect(graph_box_widget.replot_graph)
			button_box_widget.plot_button.clicked.connect(graph_box_widget.glwidget1.updateGL)

			self.show()

	app = QtGui.QApplication(sys.argv)
	window = TestWindow()
	window.show()
	app.exec_()


















