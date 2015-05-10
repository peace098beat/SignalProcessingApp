
# Gabor Wavelet Transform
Do you know wavelet transform?
Do you know Gabor?
Do you know Gaussiun?

# Pythonを使ったGaborウェーブレット変換ツール
オーディオデータ(.wav)をウェーブレット変換してみよう。
信号処理を行っていると一度は耳にしたことがあるだろう。

# 使っているツール達
Python 2.7
PyQt4
PyOpenGL
Numpy
Scipy

# モチベーション
MatplotLibに頼らない
オーディオの再生ができる。
オーディオデータを読み込む事ができる。

# GUIアプリ付き
おそらく使い勝手が悪い。
PyQtウィジェットは継承をしまくっているので注意。
MatplotlibやPyQtGraph等を使えば問題ない。

とりあえず、うまく使うなら、
AudioManagerモジュールと
gaborwaveletモジュールをインポートしてうまく使うと良い。


### AudioManagerクラス
Python2.7の標準モジュールでは、音楽データの再生と、データの読み込みが同時にできないので自作した。
使い方は簡単

	Example:
	from AudioManager import *

    file_path_1 = './audio1.wav'
    am = AudioManager(file_path_1)

    # audio play
    am.play()
    # get wave data
    w_data_1 = am.data


### Gaborウェーブレット変換
gaborwavelet.py

	from gaborwavelet import *
	from AudioManager import *

	path = './audio1.wav'
	am = AudioManager(path)

	# get wave data
	w_data = am.data
	# get normarized data
	w_data_n = am.data_n

	gwt_data = GWTAnalysis(w_data_n, Fs=am.fs)






