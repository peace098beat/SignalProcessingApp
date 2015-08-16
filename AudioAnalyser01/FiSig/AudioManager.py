# -*- coding: utf-8 -*-
"""AudioManager.py
アプリケーションのオーディオ機能を管理するクラス。
再生・信号データ・Fsの管理。

Property:
    filename:   ファイル名
    filepath:   ファイルパス
    sampwidth:  ファイルサイズ[byte]
    channels:   チャンネル数(モノラル:1,ステレオ:2)
    fs:         サンプリングレート
    framsize:   オーディオフレーム数
    data:       (Numpy Array)wavデータ配列

Method:
    play():     オーディオの再生
    set_wav():  wavファイルを設定


Example:
    file_path_1 = './audio1.wav'
    am = AudioManager(file_path_1)
    am.play()
    w_data_1 = am.data

    filepath2 = './audio2.wav'
    am.set_wav(file_path_2)
    am.play()
    w_data_2 = am.data

問題点:
    bufferをint16でしか読みだせない。
    つまり16bitオーディオしか呼び出せない。。


Reference:
    <wave: http://docs.python.jp/2/library/wave.html>
"""
import os.path
import wave

import numpy as np
import pyaudio

import sndhdr
import warnings

__author__ = "Tomoyuki Nohara <fififactory.com>"
__status__ = "production"
__version__ = "0.0.1"
__date__ = "2015.00.00"


class AudioManager(object):

    """docstring for AudioManager
    """

    def __init__(self, filepath=None):
        self.filepath = None
        self.filename = None
        self.data_raw = None
        self.data = None
        self.data_n = None
        self.wf = None

        if filepath is None:
            return

        # ファイルが存在しない場合は何もしない
        if os.path.exists(filepath):
            self.filepath = filepath
            self.filename = os.path.basename(self.filepath)
            self.set_wav(self.filepath)
        else:
            warnings.warn("file is not exists")


    def set_wav(self, filepath):
        """waveファイルの読み込み
        疑似ファイル(画像等)を.wavで読み込ますと、waveパッケージの方で
        エラーを出力してしまう。ファイル拡張子のエラーに対応している。
        """
        # ファイルが存在しない場合は返却
        if not os.path.exists(filepath):
            raise StandardError("File is not exist %s" % (filepath))
            return

        # ファイル名の取得
        filename = os.path.basename(filepath)

        if sndhdr.what(filepath)[0] is not 'wav':
            return

        # オーディオファイルであれば
        try:
            # ファイルオープン
            wf_tmp = wave.open(filepath, 'rb')
        except IOError:
            raise StandardError("Cant file load %s" % (filename))
        else:
            # 正常時の処理
            self.wf = wf_tmp
            self.filename = filename
            self.filepath = filepath
            self.__initialize()
            self.__set_data()
        finally:
            pass

    def play(self):
        """Play Audio by PyAudio
        wfの依存をなくす
        """
        if self.wf is None:
            raise StandardError("AuudioManager cant play. wave object is None")

        print '== Audio:play run.. =='
        p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(
            format=p.get_format_from_width(self.sampwidth),
            channels=self.channels,
            rate=self.fs,
            output=True,
            stream_callback=callback)

        # よくわからないが、非同期にするためにコメントアウト
        # 改善の余地あり
        # stream.start_stream()
        # while stream.is_active():
        #     import time
        #     time.sleep(0.1)
        #
        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        print '== Audio:play ..end =='

        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()

    def getFs(self):
        return self.fs

    def getData(self, mode='default'):
        if mode is "default":
            return self.data
        try:
            return self.data_raw, self.data, self.data_n
        except AttributeError:
            warnings.warn("AudioManager have not data_raw & data & data_n")
            return 0,0,0

    def __initialize(self):
        """オーディオデータの基本情報
        互換性のため、プロパティとして定義
        """
        # サンプルサイズ[byte]
        self.sampwidth = self.wf.getsampwidth()
        # チャンネル数(モノラル:1,ステレオ:2)
        self.channels = self.wf.getnchannels()
        # サンプリングレート
        self.fs = self.wf.getframerate()
        # オーディオフレーム数
        self.framsize = self.wf.getnframes()

        # wavデータの格納
        self.__set_data()
        # wevファイル上納の表示
        self.__printWaveInfo()

    def __set_data(self):
        """waveファイルをNumpy配列に変換し、
        dataプロパティに格納
        """
        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()
        # バッファの格納(バイト文字列)
        wbuffer = self.wf.readframes(self.wf.getnframes())
        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()

        # Numpy配列に変換
        # バイナリなので2バイトずつ整数(-32768-32767)にまとめる
        bit = self.sampwidth * 8
        if bit == 8:
            self.data_raw = np.frombuffer(wbuffer, dtype="int8")
        elif bit == 16:
            self.data_raw = np.frombuffer(wbuffer, dtype="int16")
        elif bit == 32:
            self.data_raw = np.frombuffer(wbuffer, dtype="int32")
        elif bit == 24:
            # 24bit データを読み込み、16bitに変換
            self.data_raw = np.frombuffer(wbuffer,'b').reshape(-1,3)[:,1:].flatten().view('i2')
        else:
            print 'Wargning!!!!!!! bit %d is none' % bit

        # 1チャンネルに変更
        self.data = []
        if self.channels == 1:
            # print 'channel 1'
            self.data = self.data_raw[:]
        if self.channels == 2:
            # print 'channel 2'
            self.data = self.data_raw[::2]

        # 正規化処理
        amp = (2. ** 8) ** self.sampwidth / 2 -1
        if self.sampwidth * 8 == 24:
            byte = 2
            amp = (2.**8) ** byte / 2 -1

        self.data_n = self.data / float(amp)

    def __printWaveInfo(self):
        """WAVEファイルの情報を表示"""
        print ""
        print "-------------------------"
        print "ファイル名:", self.filename
        print "チャンネル数:", self.wf.getnchannels()
        print "サンプル[Byte]:", self.wf.getsampwidth()
        print "サンプリング周波数:", self.wf.getframerate()
        print "フレーム数:", self.wf.getnframes()
        print "パラメータ:", self.wf.getparams()
        print "長さ（秒）:", float(self.wf.getnframes()) / self.wf.getframerate()
        print "振幅幅", (2 ** 8) ** self.sampwidth / 2 -1
        print "-------------------------"
        print ""






def main():
    path = './audio/sin_44100_24bit_stereo_5s.wav'
    am = AudioManager(path)
    am.play()

    data_raw, data, data_n = am.getData()
    print type(data)
    print len(data_raw), len(data), len(data_n)
    print max(data_raw), max(data), max(data_n)
    print min(data_raw), min(data), min(data_n)
    pass


if __name__ == '__main__':
    main()
