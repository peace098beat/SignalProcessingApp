# coding: utf-8
"""
リアルタイムIIRフィルタ
ローパスフィルタ、ハイパスフィルタ、バンドパスフィルタ、バンドストップフィルタのメソッドがある.
アルゴリズムには2次のバターワースフィルタを用いている.

Reference:
    <http://aidiary.hatenablog.com/entry/20120103/1325594723>
"""

import time
import wave
import struct
import numpy as np
from pylab import *
from submod import submod
from IIR import *
from AudioManager import *
import threading
import Queue

FRAME_SIZE = 512
IIR_a = []
IIR_b = []

p = pyaudio.PyAudio()
q = Queue.Queue()



class RealTimeIIRFilter(AudioManager):

    """リアルタイムフィルタ処理用のクラス
    """

    def play(self):
        """Play Audio by PyAudio
        """
        print '== Audio:play run.. =='

        # fs 441000
        BUFFER_SIZE = 1024*1


        def threader():
            for i in range(10):
                start_b = time.time()
                #  オーディオデータの呼び出し
                d = self.wf.readframes(BUFFER_SIZE)  # str
                # self.wf.rewind()
                # strをintに変換
                buf = np.frombuffer(d, dtype="int16")
                # フィルタリング
                data = iir(buf, IIR_a, IIR_b)  # numpy.narray
                # str形式に変換
                self.buffer = struct.pack('h' * len(data), *data)  
                print "++ buffering"
                q.put(self.buffer)

                # パフォーマンス
                elapsed_time = time.time() - start_b
                print("buffer_time:{0}".format(elapsed_time))


        # フィルタリング用のスレッドを立てる
        th = threading.Thread(target=threader, name="th")
        # フィルタリングスレッドスタート
        th.start()


        # バッファをためるための遅延
        time.sleep(0.1)
        th.join()

        # ストリームを開く
        stream = p.open(
            format=p.get_format_from_width(self.sampwidth),
            channels=self.channels,
            rate=self.fs,
            output=True,
            stream_callback=None)

        # ストリーミング開始
        stream.start_stream()

        # while stream.is_active():
        for n in range(10):
            start_p = time.time()
            # Queueからデータを取り出す
            data = q.get()
            # Queueから取り出したデータを再生
            print "-- playing"
            stream.write(data)
            # パフォーマンス
            elapsed_time = time.time() - start_p
            print("playing_time:{0}".format(elapsed_time))

        stream.stop_stream()
        stream.close()
        p.terminate()
        print '== Audio:play ..end =='

        # ファイルポインタをオーディオストリームの先頭に戻す
        self.wf.rewind()


def play_queue():
    """Queueを使ってフィルタを非同期処理する"""





if __name__ == '__main__':
    fname = "./audio/white-noise-44100hz.wav"
    # オーディオデータの呼び出し
    audio_manager = RealTimeIIRFilter(fname)
    fs = audio_manager.fs
    x = audio_manager.data.tolist()

    print 'Size of Audio x =', len(x)

    # デジタルフィルタを設計
    fc1_digital = 5000.0
    # fc2_digital = 10000.0
    fc1_analog = np.tan(fc1_digital * np.pi / fs) / (2 * np.pi)
    # fc2_analog = np.tan(fc2_digital * np.pi / fs) / (2 * np.pi)

    # フィルタ係数の算出
    a, b = createLPF(fc1_analog)
    # a, b = createHPF(fc1_analog)
    # a, b = createBPF(fc1_analog, fc2_analog)
    # a, b = createBSF(fc1_analog, fc2_analog)
    # フィルタをかける

    IIR_a = a
    IIR_b = b

    # リアルタイムフィルタ処理
    audio_manager.play()
    pass
