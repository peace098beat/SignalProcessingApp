# coding: utf-8
"""
IIRフィルタ
ローパスフィルタ、ハイパスフィルタ、バンドパスフィルタ、バンドストップフィルタのメソッドがある.
アルゴリズムには2次のバターワースフィルタを用いている.

Reference:
    <http://aidiary.hatenablog.com/entry/20120103/1325594723>
"""


import wave
import struct
import numpy as np
from pylab import *
from submod import submod


"""IIRフィルタ"""


def createLPF(fc):
    """IIR版のローパスフィルタ
    fc:カットオフ周波数
    """

    a = [0.0] * 3
    b = [0.0] * 3
    denom = 1 + 2 * np.sqrt(2) * np.pi * fc + 4 * np.pi ** 2 * fc ** 2

    b[0] = (4 * np.pi ** 2 * fc ** 2) / denom
    b[1] = (8 * np.pi ** 2 * fc ** 2) / denom
    b[2] = (4 * np.pi ** 2 * fc ** 2) / denom
    a[0] = 1.0
    a[1] = (8 * np.pi ** 2 * fc ** 2 - 2) / denom
    a[2] = (1 - (2 * np.sqrt(2) * np.pi * fc) +
            4 * np.pi ** 2 * fc ** 2) / denom

    return a, b


def createHPF(fc):
    """IIR版ハイパスフィルタ
    fc:カットオフ周波数
    """
    a = [0.0] * 3
    b = [0.0] * 3
    denom = 1 + (2 * np.sqrt(2) * np.pi * fc) + 4 * np.pi ** 2 * fc ** 2

    b[0] = 1.0 / denom
    b[1] = -2.0 / denom
    b[2] = 1.0 / denom
    a[0] = 1.0
    a[1] = (8 * np.pi ** 2 * fc ** 2 - 2) / denom
    a[2] = (1 - (2 * np.sqrt(2) * np.pi * fc) +
            4 * np.pi ** 2 * fc ** 2) / denom

    return a, b


def createBPF(fc1, fc2):
    """IIR版のバンドパスフィルタ
    fc1, fc2:カットオフ周波数
    """
    a = [0.0] * 3
    b = [0.0] * 3
    denom = 1 + 2 * np.pi * (fc2 - fc1) + 4 * np.pi ** 2 * fc1 * fc2

    b[0] = (2 * np.pi * (fc2 - fc1)) / denom
    b[1] = 0.0
    b[2] = - 2 * np.pi * (fc2 - fc1) / denom
    a[0] = 1.0
    a[1] = (8 * np.pi ** 2 * fc1 * fc2 - 2) / denom
    a[2] = (1.0 - 2 * np.pi * (fc2 - fc1) + 4 * np.pi ** 2 * fc1 * fc2) / denom

    return a, b


def createBSF(fc1, fc2):
    """IIR版のバンドストップフィルタ
    fc1, fc2:カットオフ周波数
    """
    a = [0.0] * 3
    b = [0.0] * 3
    denom = 1 + 2 * np.pi * (fc2 - fc1) + 4 * np.pi ** 2 * fc1 * fc2

    b[0] = (4 * np.pi**2 * fc1 * fc2 + 1) / denom
    b[1] = (8 * np.pi**2 * fc1 * fc2 - 2) / denom
    b[2] = (4 * np.pi**2 * fc1 * fc2 + 1) / denom
    a[0] = 1.0
    a[1] = (8 * np.pi**2 * fc1 * fc2 - 2) / denom
    a[2] = (1 - 2*np.pi * (fc2 - fc1) + 4 * np.pi**2 * fc1 * fc2) / denom

    return a, b

def iir(x, a, b):
    """IIRフィルタをかける.
	x: 入力信号
	a,b: フィルタ係数"""

    # フィルタの出力信号
    y = [0.0] * len(x)
    Q = len(a) - 1
    P = len(b) - 1

    """ TODO: 高速化が必要"""
    for n in range(len(x)):

        y[n] = np.sum([b[i]*x[n-i] for i in range(0, P+1) if n-i >= 0])
        # for i in range(0, P + 1):
        # if n - i >= 0:
        # y[n] += b[i] * x[n - i]
        y[n] = y[n] - np.sum([a[j]*y[n-j] for j in range(1,Q+1) if n-j >= 0])
        # for j in range(1, Q + 1):
        # if n - j >= 0:
        # y[n] -= a[j] * y[n - j]

    return y

def save(data, fs, bit, filename):
    submod.save(data, fs, bit, filename)

def H2(f, a, b):
    nume = b[0] + b[1] * np.exp(-2j * np.pi * f) + b[2] * np.exp(-4j * np.pi * f)
    deno = 1 + a[1] * np.exp(-2j * np.pi * f) + a[2] * np.exp(-4j * np.pi * f)
    val = nume / deno
    return np.sqrt(val.real**2 + val.imag**2)

def main():
    wf = wave.open("./audio/white-noise-44100hz.wav", "r")
    fs = wf.getframerate()

    x = wf.readframes(wf.getnframes())
    x = frombuffer(x, dtype="int16") / (2.0**16) /2

    # デジタルフィルタを設計
    fc1_digital = 5000.0
    fc2_digital = 10000.0
    fc1_analog = np.tan(fc1_digital * np.pi / fs) / (2 * np.pi)
    fc2_analog = np.tan(fc2_digital * np.pi / fs) / (2 * np.pi)

    # フィルタ係数の算出
    # a, b = createLPF(fc1_analog)
    a, b = createHPF(fc1_analog)
    # a, b = createBPF(fc1_analog, fc2_analog)
    # a, b = createBSF(fc1_analog, fc2_analog)
    print a, b

    # フィルタをかける
    y = iir(x, a, b)
    _y = [int(v * (2.0**16)) for v in y]
    _y = struct.pack("h" * len(_y), *_y)
    save(_y, fs, 16, "./audio/white_noise2.wav")


    # 伝達関数Hの周波数特性
    amp = []
    # for f in range(0, fs/2):
    # f = float(f) / fs
    # amp.append(H2(f, a, b))
    amp = [H2(float(f)/fs,a,b) for f in range(0, fs/2)]

    # フィルタの伝達特性のプロット
    subplot(4,1,1)
    plot(x)

    subplot(4,1,2)
    plot(range(0, fs/2), amp)
    title('IIR Filter')

    subplot(4,1,3)
    plot(y)
    show()

    submod.fft(x, fs)
    submod.fft(y, fs)

if __name__ == '__main__':
    main()