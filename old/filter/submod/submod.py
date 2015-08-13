# -*- coding: utf-8 -*-

import numpy as np
import wave
from pylab import *


def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()


def play(data, fs, bit):
    """オーディオ再生関数
    data: str(ファイルではない)
    """

    import pyaudio
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output=True)
    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    # 再生位置ポインタ
    sp = 0
    buffer = data[sp:sp+chunk]
    while buffer != '':
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp+chunk]
    stream.close()
    p.terminate()



def printWaveInfo(wf):
    """WAVEファイルの情報を表示"""
    print ""
    print "-------------------------"
    print "チャンネル数:", wf.getnchannels()
    print "サンプル[Byte]:", wf.getsampwidth()
    print "サンプリング周波数:", wf.getframerate()
    print "フレーム数:", wf.getnframes()
    print "パラメータ:", wf.getparams()
    print "長さ（秒）:", float(wf.getnframes()) / wf.getframerate()
    print "振幅幅", (2 ** 8) ** wf.getsampwidth() / 2
    print "-------------------------"
    print ""


def fft(x, fs):
    start = 0
    N = 512

    try:
        x.append(0.0)
    except:
        x = x.tolist()

    for i in range(N):
        x.append(0.0)

    X = np.fft.fft(x[start:start + N])
    freqList = np.fft.fftfreq(N, d=1.0 / fs)

    amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]

    subplot(211)
    plot(range(start, start + N), x[start:start + N])
    axis([start, start + N, -0.5, 0.5])
    xlabel("time [sample]")
    ylabel("ampiltude")

    subplot(212)
    n = len(freqList) / 2
    plot(freqList[:n], amplitudeSpectrum[:n], linestyle='-')
    xlim([0, fs / 2])
    xlabel("freqency [Hz]")
    ylabel("ampiltude spectrum")

    show()

    return X
