# -*- coding: utf-8 -*-
"""GaborWavelet.py
ガボール変換を使ったウェーブレット変換

Version:
    1.0


Reference:
    http://hp.vector.co.jp/authors/VA046927/gabor_wavelet/gabor_wavelet.html
    http://criticaldays2.blogspot.jp/2014/04/blog-post_23.html
    http://www.softist.com/programming/gabor-wavelet/gabor-wavelet.htm
"""
import numpy as np

def gwt(audio_data, Fs):

    def psi(a, b, a_t, sigma):
        """ ガボール関数"""
        t = (a_t - b) / a
        g = 1. / (2 * np.sqrt(np.pi * sigma)) * np.exp(-1. * t ** 2 / (4. * sigma ** 2))
        e = np.exp(1j * 2. * np.pi * t)
        return g * e


    def utili_sample(a, sigma):
        Vc = 0.01
        samp = a * sigma * np.sqrt(-2. * np.log(Vc))
        return samp

    import time
    start = time.time()

    Fs = 1. * Fs
    adata = audio_data
    N = len(adata)

    """
    信号選択: 人工信号の生成 or オーディオ信号
    """
    sweep = 0
    if sweep == 1:
        import scipy.signal
        tary = np.linspace(0, 1. * N / Fs, N)
        f0 = 1.
        f1 = 22000.
        t1 = 1. * N / Fs
        X = scipy.signal.chirp(tary, f0, t1, f1)
    elif sweep == 2:
        t = np.linspace(0, 1, N)
        f1 = 500
        s1 = np.sin(2 * np.pi * f1 * t)
        s1[0:np.floor(N / 2)] = 0

        f2 = 2000
        s2 = np.sin(2 * np.pi * f2 * t)
        s2[np.floor(N / 2):] = 0

        X = np.array(s1 + s2)
    elif sweep == 3:
        t = np.linspace(0, 1, N)
        X = np.zeros_like(t)
        X[np.floor(N / 2) - 5:np.floor(N / 2) + 5] = 1
    elif sweep == 4:
        t = np.linspace(0, 1, N)
        f1 = 500
        s1 = np.sin(2 * np.pi * f1 * t)
        s1[0:np.floor(N / 2)] = 0

        f2 = 2000
        s2 = np.sin(2 * np.pi * f2 * t)
        s2[np.floor(N / 2):] = 0

        s3 = np.zeros_like(t)
        w = 100
        s3[np.floor(N / 2) - w: np.floor(N / 2) + w] = 1

        # X = np.array(s1 + s2 + s3)
        X = np.array(s3)
    else:
        X = np.array(adata) * 1.

    # -------------------
    # ウェーブレット変換処理
    # -------------------
    """
        解析パラメータ
    """
    # 1. ガボールウェーブレットパラメータ
    sigma = 5
    # 2. 周波数分割数
    a_N = 128*2
    # 解析周波数(最低周波数)
    f_min = 1
    # 解析周波数(最高周波数)
    f_max = Fs/2

    # ループ準備
    # ---------
    # 時間幅
    t = np.arange(0, N) / float(Fs)
    # 解析周波数
    fn = np.linspace(f_min, f_max, a_N)
    # 解析結果格納バッファ
    Anadata = np.empty(shape=(N, a_N), dtype=complex)

    print "-----------------------------"
    print '== Gabor Wavelet Analysing =='
    print '== ...'
    for a_n in range(0, a_N):
        a = 1. / fn[a_n]
        b = 1. * N / 2. / Fs
        Psi = psi(a, b, t, sigma)

        # 実用領域のみ畳み込み
        us = np.floor(utili_sample(a, sigma) * Fs)
        if us < N:
            ss = np.floor((N - us) / 2)
            Psi = Psi[ss:ss + us]

        # 畳み込み (convolve)
        Anadata[:, a_n] = (1. / np.sqrt(a)) * np.convolve(Psi, X, 'same')

    # 描画用に配列の左右を入れ替え
    # Anadata = np.fliplr(Anadata)

    # 解析時間
    print("== Finish Analys :{0}".format(time.time() - start))
    print "-----------------------------"

    return Anadata, t, fn




# ******************************************
#
#  Demo
#
# ******************************************
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    filename = 'guitar_A4.wav'

    # オーディオのロード
    from scipy.io.wavfile import read
    fs, data = read(filename)
    data = data[0:fs/2-1]

    # GWT解析
    gwt_data = gwt(data, Fs=fs)
    gdata, trange, frange = np.abs(gwt_data)
    gdata = 20*np.log10(gdata)

    # STFTの表示
    fig2 = plt.figure()
    ax2 = fig2.gca()
    plt.specgram(data, NFFT=512, noverlap=256, Fs=fs, cmap='jet', scale='dB', mode='magnitude', vmin=0, vmax=120)
    plt.colorbar()
    plt.title('specgram (STFT)')

    # Scarogramの表示
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    extent = 0, (fs/2.-1)/fs, 0, fs/2
    gdata = np.flipud(gdata.T)
    img = plt.imshow(gdata, cmap='jet', extent=extent, vmin=0, vmax=120)
    plt.colorbar()
    ax3.set_title('scarogram (GWT)')
    ax3.axis('auto')


    plt.show()

