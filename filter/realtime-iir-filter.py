# coding: utf-8
"""
リアルタイムIIRフィルタ
ローパスフィルタ、ハイパスフィルタ、バンドパスフィルタ、バンドストップフィルタのメソッドがある.
アルゴリズムには2次のバターワースフィルタを用いている.

Reference:
    <http://aidiary.hatenablog.com/entry/20120103/1325594723>
TODO:
    リアルタイム?でのフィルタ処理を実装
    Scipyの利用で再生よりもフィルタリング時間の方が短くなった
    Cの早さを実感。
    スレッドを使っての実装も何となくわかったがまだ勉強が必要
    しかし、本質は、play自体をスレッド処理しなければいけない。
    いまのままだと、再生中は結局同期処理をしている.
    そろそろ設計図が必要

"""

import time
import threading
import Queue
import scipy
import scipy.signal

from AudioManager import *

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
            for i in range(100):
                # 時間計測
                start_b = time.time()
                #  オーディオデータの呼び出し
                d = self.wf.readframes(BUFFER_SIZE)  # str
                # self.wf.rewind()
                # strをintに変換
                buf = scipy.fromstring(d, scipy.int16)
                # フィルタリング
                data = scipy.signal.lfilter(IIR_b, IIR_a, buf)
                # strに変換
                self.buffer = scipy.int16(data).tostring()
                # print "++ buffering"
                q.put(self.buffer)

                # パフォーマンス
                elapsed_time = time.time() - start_b
                print("buffer_time:{0}".format(elapsed_time))


        # フィルタリング用のスレッドを立てる
        th = threading.Thread(target=threader, name="th")
        # フィルタリングスレッドスタート
        th.start()


        # バッファをためるための遅延
        # time.sleep(0.1)
        # th.join()

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
        for n in range(100):
            start_p = time.time()
            # Queueからデータを取り出す
            data = q.get()
            # Queueから取り出したデータを再生
            # print "-- playing"
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
    fname = "./audio/sine.wav"

    # オーディオデータの呼び出し
    audio_manager = RealTimeIIRFilter(fname)
    fs = audio_manager.fs
    x = audio_manager.data.tolist()

    print 'Size of Audio x =', len(x)

    # デジタルフィルタを設計

    fsamp = fs
    fpass = 5000.0
    fstop = 6000.0
    wp = fpass / (fsamp / 2.0 )
    ws = fstop / (fsamp / 2.0 )
    wp = 0.2
    ws = 0.5
    IIR_b, IIR_a = scipy.signal.iirdesign(wp,ws,1,30)

    # リアルタイムフィルタ処理
    audio_manager.play()

