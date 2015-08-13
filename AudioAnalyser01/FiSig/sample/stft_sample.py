
# -*- coding: utf-8 -*-
"""
sox な感じにスペクトログラムを表示する。
"""
from scipy import hanning, hamming, histogram, log10
from matplotlib import pylab as pl

def _wavread_scipy(filename):
    print 'wavread_scipy'
    from scipy.io.wavfile import read

    fs, data = read(filename)

    print "Sampling rate :", fs
    print data.ndim

    if data.ndim == 1:
        return data, fs
    elif data.ndim == 2:
        left = data[:, 0]
        right = data[:, 1]
        return left, fs

# ==================================
#
#    Short Time Fourier Trasform
#
# ==================================
from scipy import ceil, complex64, float64, hamming, zeros
from scipy.fftpack import fft# , ifft
from scipy import ifft # こっちじゃないとエラー出るときあった気がする
from scipy.io.wavfile import read

from matplotlib import pylab as pl

# ======
#  STFT
# ======
"""
x : 入力信号(モノラル)
win : 窓関数
step : シフト幅
"""
def stft(x, win, step):
    l = len(x) # 入力信号の長さ
    N = len(win) # 窓幅、つまり切り出す幅
    M = int(ceil(float(l - N + step) / step)) # スペクトログラムの時間フレーム数

    new_x = zeros(N + ((M - 1) * step), dtype = float64)
    new_x[: l] = x # 信号をいい感じの長さにする

    X = zeros([M, N], dtype = complex64) # スペクトログラムの初期化(複素数型)
    for m in xrange(M):
        start = step * m
        X[m, :] = fft(new_x[start : start + N] * win)
    return X


# =================================
#  sox な感じにスペクトログラム表示
# =================================
def imshow_sox(spectrogram, rm_low = 0.1):
    max_value = spectrogram.max()
    ### amp to dbFS
    db_spec = log10(spectrogram / float(max_value)) * 20
    ### カラーマップの上限と下限を計算
    hist, bin_edges = histogram(db_spec.flatten(), bins = 1000, normed = True)
    hist /= float(hist.sum())
    pl.hist(hist)
    pl.show()
    S = 0
    ii = 0
    while S < rm_low:
        S += hist[ii]
        ii += 1
    vmin = bin_edges[ii]
    vmax = db_spec.max()

    pl.imshow(db_spec, origin = "lower", aspect = "auto", cmap = "hot", vmax = vmax, vmin = vmin)



if __name__ == "__main__":
    import wave
    import numpy as np
    wavfile = "../../golf_D.wav"
    wf = wave.open(wavfile, "r")
    fs = wf.getframerate()
    byte = wf.getsampwidth()
    chn = wf.getnchannels()
    x_t = wf.readframes(wf.getnframes())
    x = np.frombuffer(x_t, dtype="int16") / (2.0 ** 8) ** byte


    # # data, fs = _wavread_scipy(wavfile)
    data = x[:2000]
    # ### STFT
    fftLen = 512
    win = hanning(fftLen)
    step = fftLen / 8
    spectrogram = abs(stft(data, win, step)[:, : fftLen / 2 + 1]).T

    ### 表示
    fig = pl.figure()
    fig.patch.set_alpha(0.)
    imshow_sox(spectrogram)
    pl.tight_layout()
    pl.show()




   