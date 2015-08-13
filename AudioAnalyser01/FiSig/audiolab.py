# -*- coding: utf-8 -*-
"""
.wavファイルを扱うための関数群

    wavread(filepath)
    # .wavファイルを読み込み、numpy.arrayとして返却


"""
import sys
import wave
import numpy as np

def wavread(filename):
    print 'waveread'

    # [data, fs]=wavread_wave(filename)
    [data, fs]= _wavread_scipy(filename)

    return data, fs


def _wavread_wave_old(filename):
    """ .wavファイルを読み込み、numpy.arrayとして返却
    """
    wf = wave.open(filename, "r")
    # サンプリングレート
    fs = wf.getframerate()
    # チャンネル数
    channels = wf.getnchannels()
    # オーディオフレーム数
    framsize = wf.getnframes()
    # バッファの呼び出し
    x = wf.readframes(framsize)
    # 量子化bit数
    bit = wf.getsampwidth()
    # 振幅の正規化[-1,1]
    amp = (2. ** 8) ** bit / 2.


    __printWaveInfo(wf, filename)

    # Numpy配列に変換
    # バイナリなので2バイトずつ整数(-32768, 32767)にまとめる
    # data = np.frombuffer(x, dtype="int16") / amp
    # data = np.frombuffer(x, count=-1)
    # よくわからないけど、量子化bit数で分割
    if bit == 1:
        data = np.frombuffer(x, dtype="int8") / amp
    if bit == 2:
        data = np.frombuffer(x, dtype="int16") / amp
    if bit == 3:
        data = np.frombuffer(x, dtype="int24") / amp
    if bit == 4:
        data = np.frombuffer(x, dtype="int32") / amp
    print data


    def __printWaveInfo(wf, filename):
        """WAVEファイルの情報を表示"""
        print u""
        print u"-------------------------"
        print u"ファイル名:", filename
        print u"チャンネル数:", wf.getnchannels()
        print u"サンプル[Byte]:", wf.getsampwidth()
        print u"サンプリング周波数:", wf.getframerate()
        print u"フレーム数:", wf.getnframes()
        print u"パラメータ:", wf.getparams()
        print u"長さ（秒）:", float(wf.getnframes()) / wf.getframerate()
        print u"振幅", (2 ** 8) ** wf.getsampwidth() / 2
        print u"-------------------------"
        print u""
    # ポインタのクローズ
    wf.close()

    return data, float(fs)

def _wavread_wave(filename):
    import wave
    import struct
    a = wave.open(filename)
    # a.getnchannels()
    # a.getsampwidth()
    fs = a.getframerate()
    # a.getnframes()
    d = a.readframes(a.getnframes())
    p = a.getparams()
    # ファイルをunpack
    data = struct.unpack('%dh' % a.getnframes(), d)
    print data[0:10]

    return data, fs


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

