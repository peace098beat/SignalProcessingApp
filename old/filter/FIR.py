# coding: utf-8
"""
FIRフィルタ
ローパスフィルタ、ハイパスフィルタ、バンドパスフィルタ、バンドストップフィルタのメソッドがある.


"""

import wave
import numpy as np
from pylab import *
from submod.submod import *


FRAME_SIZE = 512


def sinc(x):
    if x == 0.0:
        return 1.0
    else:
        return np.sin(x) / x


def createLPF(fe, delta):
    """ローパスフィルタを設計する関数
    fe: エッジ周波数
    delta: 遷移帯域幅
    遷移帯域幅を満たすフィルタ係数の数を計算
    N+1が奇数になるように調整が必要
    """

    # 臨海帯域幅から必要なサンプル数(フィルタ係数)を算出
    N = round(3.1 / delta) - 1.
    # N+1を奇数にする
    if (N + 1) % 2 == 0:
        N += 1
    N = int(N)

    # derived filter coefficient
    b = []
    for i in range(-N / 2, N / 2 + 1):
        b.append(2.0 * fe * sinc(2.0 * math.pi * fe * i))

    # ハニング窓関数をかける(窓関数法)
    hanningWindow = np.hanning(N + 1)
    for i in range(len(b)):
        b[i] *= hanningWindow[i]

    return b


def createHPF(fe, delta):
    """ハイパスフィルタを設計
    fe: エッジ周波数, delta: 遷移帯域幅"""

    # フィルタ係数の数を算出
    N = round(3.1 / delta) - 1
    print 'HPF:N=', N
    # 係数の数を奇数にそろえる
    if (N + 1) % 2 == 0:
        N += 1
    N = int(N)

    # フィルタ係数を求める
    b = [sinc(math.pi * i) - 2 * fe * sinc(2 * math.pi * fe * i)
         for i in range(-N / 2, N / 2 + 1)]

    # ハニング窓をかける(窓関数法)
    hanningWindow = np.hanning(N + 1)
    for i in range(len(b)):
        b[i] *= hanningWindow[i]

    return b


def createBPF(fe1, fe2, delta):
    """バンドパスフィルタの設計, fe1:エッジ周波数(低), fe2:エッジ周波数(高), delta:遷移帯域幅"""

    # フィルタ係数の数を算出
    N = round(3.1 / delta) - 1
    print N
    # 係数の数を奇数にそろえる
    if (N + 1) % 2 == 0:
        N += 1
    N = int(N)
    print N

    # フィルタ係数を求める
    b = [2 * fe2 * sinc(2 * math.pi * fe2 * i) - 2 * fe1 *
         sinc(2 * math.pi * fe1 * i) for i in range(-N / 2, N / 2 + 1)]

    # ハニング窓をかける(窓関数法)
    hanningWindow = np.hanning(N + 1)
    for i in range(len(b)):
        b[i] *= hanningWindow[i]

    return b


def createBSF(fe1, fe2, delta):
    """バンドストップフィルタの設計, fe1:エッジ周波数(低), fe2:エッジ周波数(高), delta:遷移帯域幅"""

    # フィルタ係数の数を算出
    N = round(3.1 / delta) - 1
    # 係数の数を奇数にそろえる
    if (N + 1) % 2 == 0:
        N += 1
    N = int(N)

    # フィルタ係数を求める
    b = [sinc(math.pi * i) - 2 * fe2 * sinc(2 * math.pi * fe2 * i) + 2 *
         fe1 * sinc(2 * math.pi * fe1 * i) for i in range(-N / 2, N / 2 + 1)]

    # ハニング窓をかける(窓関数法)
    hanningWindow = np.hanning(N + 1)
    for i in range(len(b)):
        b[i] *= hanningWindow[i]

    return b


def fir(x, b):
    """FIR filtering
    x: in signal
    b: filter coefficient
    """

    y = [0.0] * len(x)
    N = len(b) - 1
    for n in range(len(x)):
        for i in range(N + 1):
            if n - i >= 0:
                y[n] += b[i] * x[n - i]

    return y


if __name__ == '__main__':
    # wf = wave.open("./audio/white_noise.wav", "r")
    wf = wave.open("./audio/white-noise-44100hz.wav", "r")
    printWaveInfo(wf)
    fs = wf.getframerate()
    byte = wf.getsampwidth()
    chn = wf.getnchannels()
    x_t = wf.readframes(FRAME_SIZE)
    x = frombuffer(x_t, dtype="int16") / (2.0 ** 8) ** byte

    # グラフ
    # fft(x.tolist(),fs)

    # 正規化したエッジ周波数
    fe = 10000.0 / fs
    # 正規化した遷移帯域幅
    delta = 1000.0 / fs

    # LPFを設計
    b = createLPF(fe, delta)
    # HPFを設計
    c = createHPF(fe, delta)
    # BPFを設計
    fe1 = 1000.0 / fs
    fe2 = 3000.0 / fs
    delta = 1000.0 / fs
    d = createBPF(fe1, fe2, delta)
    # BSFを設計
    e = createBSF(fe1, fe2, delta)
    fft(e, fs)

    # フィルタをかける
    y_b = fir(x, b)
    y_c = fir(x, c)
    y_d = fir(x, d)
    y_e = fir(x, e)
    fft(y_e, fs)

    # 音声を保存
    # save(y, fs, 16, "white_noise_low_pass.wav")
