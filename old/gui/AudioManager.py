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

Reference:
    <wave: http://docs.python.jp/2/library/wave.html>
"""
import os.path
import wave

import numpy as np
import pyaudio


__author__ = "Tomoyuki Nohara <fififactory.com>"
__status__ = "production"
__version__ = "0.0.1"
__date__ = "2015.00.00"


class AudioManager(object):

    """docstring for AudioManager
    """
    # CHUNK = 1024

    def __init__(self, filepath=None):
        # Debug
        if filepath == None:
            self.filepath = './audio/golf_D.wav'
        else:
            self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        self.set_wav(self.filepath)

    def set_wav(self, filepath):
        """waveファイルの読み込み
        疑似ファイル(画像等)を.wavで読み込ますと、waveパッケージの方で
        エラーを出力してしまう。ファイル拡張子のエラーに対応している。
        """
        print '== AudioManager::set_wav =='
        if os.path.exists(filepath):
            print 'ファイルが存在しました。', filepath
            filename = os.path.basename(filepath)

            # ファイルが存在する場合の処理
            root, ext = os.path.splitext(filepath)
            # ext = '.wav'
            if ext == '.wav' or ext == '.wave':
                # オーディオファイルであれば
                try:
                    # ファイルオープン
                    wf_tmp = wave.open(filepath, 'rb')
                except Exception, e:
                    print ""
                    print "++++++++++++++++++++++++++++++++++++++++"
                    print 'WARNING: wavファイルの読み込みに失敗しました.'
                    print filename
                    print type(e)
                    print e
                    print "++++++++++++++++++++++++++++++++++++++++"
                    # raise
                    pass
                else:
                    # 正常時の処理
                    self.wf = wf_tmp
                    self.filename = filename
                    self.filepath = filepath
                    self.__initialize()
                    self.__set_data()
                finally:
                    pass
        else:
            print 'ファイルは存在しません'
            print filepath

    def play(self):
        """Play Audio by PyAudio
        wfの依存をなくす
        """
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

        stream.start_stream()
        while stream.is_active():
            import time
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        p.terminate()
        print '== Audio:play ..end =='

        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()


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
        self.data_raw = np.frombuffer(wbuffer, dtype="int16")

        # 1チャンネルに変更
        self.data = []
        if self.data_raw.ndim == 1:
            self.data = self.data_raw[:]
        if self.data_raw.ndim == 2:
            self.data = self.data_raw[:, 0]
            # self.data = self.data_raw[:,1]
            # self.data = self.data_raw[:,0] + self.data_raw[:,1]

        # 正規化処理
        amp = (2. ** 8) ** self.sampwidth / 2
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
        print "振幅幅", (2 ** 8) ** self.sampwidth / 2
        print "-------------------------"
        print ""


def main():
    path = './audio/golf_D.wav'
    am = AudioManager(path)
    am.play()
    # path = './audio/music1.wav'
    path = './audio/M1F1-int16WE-AFsp.wav'
    am.set_wav(path)
    am.play()
    wave_data = am.data
    amp = float((2 ** 8) ** am.sampwidth / 2)
    wave_data = wave_data / float(amp)
    print wave_data
    print max(wave_data)


if __name__ == '__main__':
    main()

dumy = 1
dumy = 2
