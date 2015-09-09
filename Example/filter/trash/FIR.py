# -*- coding: utf-8 -*-

import wave
import struct
import numpy as np
import scipy
from pylab import *


Fs = 441000
BIT = 16


def createWhiteNoise():
    freqList = [float(f) for f in range(1, 2000, 10)]
    A = 1.0
    fs = 8000
    length = 1.0
    bit = 16
    data = createCombinedWave(A, freqList, fs, length)
    save(data, fs, bit, "white_noise.wav")


def createCombinedWave(A, freqList, fs, length):
    """freqListの正弦波を合成した波を返す"""
    A = float(fs)
    fs = float(fs)
    length = float(length)

    data = []
    amp = float(A) / len(freqList)
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in arange(length * fs):  # nはサンプルインデックス
        s = 0.0

        # for f in freqList:
        # s += amp * np.sin(2 * np.pi * f * n / fs)

        # リファクタリング
        s = sum([amp*np.sin(2*np.pi*f*n/fs) for f in freqList])

        # 振幅が大きい時はクリッピング
        if s > 1.0:
            s = 1.0
        if s < -1.0:
            s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    play(data, fs, 16)
    return data


def createSineWave(A, f0, fs, length):
    """振幅A、基本周波数f0、サンプリング周波数 fs、
    長さlength秒の正弦波を作成して返す"""
    data = []
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in arange(length * fs):  # nはサンプルインデックス
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        # 振幅が大きい時はクリッピング
        if s > 1.0:
            s = 1.0
        if s < -1.0:
            s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換(2**8)**2=16bit
    data = [int(x * 32767.0) for x in data]
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data


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


def save(data, fs, bit, filename):
    """波形データをWAVEファイルへ出力"""
    wf = wave.open(filename, "w")
    wf.setnchannels(1)
    wf.setsampwidth(bit / 8)
    wf.setframerate(fs)
    wf.writeframes(data)
    wf.close()


def createSignal():
    freqList = [262, 294, 330, 349, 392, 440, 494, 523]

    data = createCombinedWave(
        A=1.0,
        freqList=freqList,
        fs=8000,
        length=1.0)
    save(data, 8000, 16, "combined_sine.wav")

    return data


def fir(x, b):
    """FIRフィルタ
    x: 入力信号
    b: フィルタ係数"""
    y = [0.0] * len(x)  # フィルタ出力信号
    N = len(b) - 1
    for n in range(len(x)):
        for i in range(N+1):
            if n - i >= 0:
                y[n] += b[i] * x[n-i]
    return y


if __name__ == "__main__":

    createWhiteNoise()

    # 生成したオーディオの読み込み
    wf = wave.open("combined_sine.wav", "r")
    wf = wave.open("white_noise.wav", "r")
    fs = wf.getnframes()

    # 正規化
    _x = wf.readframes(wf.getnframes())
    x = frombuffer(_x, dtype="int16") / ((2.0**8)**2) / 2.0

    # FIRフィルタをかける
    b = [0.5, 0.5]
    # b = [0.1]*10
    # b = [0.2]*5
    y = fir(x, b)

    y_fft = np.fft.fft(y)
    y_fft_r = np.real(y_fft)
    y_fft_amp = np.abs(y_fft)

    # f1 = figure()
    m = 4
    n = 1
    subplot(m, n, 1)
    plot(x)
    axis([1000, 2000, -1, 1])

    subplot(m, n, 2)
    gdata = np.abs(np.fft.fft(x))
    plot(gdata)
    xlim([0, fs/2.])

    subplot(m, n, 3)
    plot(y)
    axis([1000, 2000, -1, 1])

    subplot(m, n, 4)
    plot(y_fft_amp)
    xlim([0, fs/2.])
    show()

    # waveファイルとして保存するために、正規か前のバイナリに戻す
    y = [int(v * 32767.0) for v in y]
    y = struct.pack("h" * len(y), *y)
    save(y, fs, 16, "fir_combined_sine.wav")
