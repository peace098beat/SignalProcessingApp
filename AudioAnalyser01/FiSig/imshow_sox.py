# -*- coding: utf-8 -*-
"""
sox な感じにスペクトログラムを表示する。
"""
from scipy import hanning, hamming, histogram, log10
# from scikits.audiolab import wavread
from audiolab import wavread
from matplotlib import pylab as pl

from stft import stft

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
 
    ax = pl.imshow(db_spec, origin = "lower", aspect = "auto", cmap = "hot", vmax = vmax, vmin = vmin)
    return ax
    

def test():
    wavfile = "../golf_D.wav"
    data, fs  = wavread(wavfile)



    ### STFT
    fftLen = 1024
    win = hanning(fftLen)
    step = fftLen / 8
    spectrogram = abs(stft(data, win, step)[:, : fftLen / 2 + 1]).T

    ### 表示
    fig = pl.figure()
    fig.patch.set_alpha(0.)
    imshow_sox(spectrogram)
    pl.tight_layout()
    pl.show()

if __name__ == "__main__":
    test()