# -*- coding: utf-8 -*-

## 必要なモジュールをインポート
import os
import sys

## PySide系モジュール
from PySide.QtGui import *
from PySide.QtCore import *

## 演算系モジュール
import numpy as np

## GUIモジュール
from MasterOfMainWindow import MasterOfMainWindow
from UI_SignalAnalyser import Ui_MainWindow

## FiSigモジュール
from FiSig.AudioManager import AudioManager
from FileListWidget import FileListWidget
## uiファイル名
# uiFile = 'UI_SignalAnalyser.ui'

## グローバル変数
audio_manager = AudioManager()


# =============================================================================
## GUIの構築
class GUI(MasterOfMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        MasterOfMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # CSSをセット
        self.setCSS()
        # ====================================
        # ステータスバーにプログラスバーを追加
        #  (qtDesignerでの作り方がわからない)
        # ====================================
        self.progressBar = QProgressBar()
        self.statusbar.addPermanentWidget(self.progressBar)
        self.progressBar.reset()
        self.progressBar.setVisible(False)
        self.progressBar.setValue(10)

        # ====================================
        # モデルとデリゲートを生成
        # ====================================
        self.fileloaded.connect(self.flashStatusBar)
        self.fileloaded.connect(self._subroutin)
        self.connect(self.myListView, SIGNAL("clicked(QModelIndex)"), self.slot1)

    def setCSS(self):
        """
        同じフォルダにあるcssを読みこんでセット
        """
        with open("style.css","r") as f:
            self.setStyleSheet("".join(f.readlines()))

    # ==========================================
    # Slotの設定
    # ==========================================
    @Slot()
    def slot1(self, index):
        print 'listslot'
        print index.row()
        print index.data(Qt.DisplayRole)
        name = index.data(Qt.DisplayRole)
        self.cahangeFilePath(name)

    @Slot()
    @Slot(str)
    def flashStatusBar(self, fstring):
        self.statusbar.showMessage(fstring)

    @Slot()
    def setAudioFile(self):
        audio_manager.set_wav(self.abspath)
        self.flashStatusBar("Set Audio File : %s" % self.abspath)

    @Slot()
    def playAudio(self):
        audio_manager.play()
        pass

    @Slot()
    def analys(self):
        import time
        from scipy import hanning
        from FiSig.gwt import gwt
        from FiSig.stft import stft

        self.statusbar.showMessage("analysing ..", 5000)

        # -- progress bar --
        self.progressBar.setVisible(True)
        self.progressBar.setValue(10)

        # オーディオファイルのロード
        am = AudioManager(self.abspath)
        fs = am.getFs()
        data = am.getData()

        # --- データを格納 ---
        self.fs = fs

        ############################################
        # wave
        ############################################
        # DEBUG: データが長いと面倒なので、0.5sだけ抜き出す
        # if len(data) >= fs/4:
        #     data = data[0:fs/2 - 1]

        data = data[fs/2/6:fs/2/3 - 1]
        N = len(data)

        wave_trange = np.arange(N)/float(fs)


        # --- データを格納 ---
        self.wave_d = data
        self.wave_trange = wave_trange
        # -- progress bar --
        self.progressBar.setValue(30)
        ############################################
        # STFT
        ############################################
        # fftLen = 512
        # win = hanning(fftLen)
        # step = fftLen / 2
        # spectrogram = abs(stft(data, win, step)[:, : fftLen / 2 + 1]).T
        # spectrogram = 20 * np.log10(spectrogram)
        #
        # # --- データを格納 ---
        # self.spec_d = spectrogram
        # -- progress bar --
        self.progressBar.setValue(60)

        ############################################
        # GWT
        ############################################
        # GWTは解析時間が長いので、解析時間を表示
        # self.statusbar.showMessage("GWT running ..", 5000)
        # 時間計測開始
        # start = time.time()

        # GWT解析を実行する
        d_gwt, trange, frange = gwt(data, Fs=fs)

        # d_gwt = 20 * np.log10(np.abs(d_gwt))
        # d_gwt = 20 * np.log10(np.abs(d_gwt))
        d_gwt = np.abs(d_gwt)
        extent = trange[0], trange[-1], frange[0], frange[-1]

        # -- progress bar --
        self.progressBar.setValue(80)

        # --- データを格納 ---
        self.gwt_d = d_gwt
        self.gwt_trange = trange
        self.gwt_frange = frange
        self.gwt_extent = extent

        # 解析終了と、解析時間を表示する
        # self.statusbar.showMessage("GWT fin ... analys time %0.2f[s]" % (time.time() - start), 10000)
        # -- progress bar --
        self.progressBar.setValue(100)
        self.progressBar.setVisible(False)

    @Slot()
    def plot(self):
        self.flashStatusBar("Call plot")
        self.figure1.plot(ydata=self.wave_d, xdata=self.wave_trange)
        self.figure2.plot(zdata=self.gwt_d[::10,:], extent=self.gwt_extent)
        self.figure3.plot(atTime=1, zdata=self.gwt_d, trange=self.gwt_trange, frange=self.gwt_frange)

        pass

    @Slot()
    def _subroutin(self):
        self.analys()
        self.plot()

    def dropEvent(self, event):
        """ドロップイベントの検知
        MasterMainWindowメソッドの継承
        """
        print 'dropEvent'

        urls = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]

        # リストを消去
        self.myListView.clearItems()

        import glob

        # 各URLをリストに追加する
        for url in urls:
            # URLがフォルダかファイルかを判定
            if os.path.isdir(url):
                # パスを正規化
                abspath = os.path.abspath(url)
                print 'This is Dir : ', abspath
                # フォルダ直下の.wavを検索
                searchpath = os.path.join(abspath, '*.wav')
                # ディレクトリ直下のファイルを呼び出す
                files = [r for r in glob.glob(searchpath)]
                # ファイルリストから一つずつリストに追加
                for file in files:
                    self.myListView.addItem({u"name": file})

            else:
                # URLがファイルの場合、(.wav)だけをリストにつか
                abspath = os.path.abspath(url)
                # 拡張子を取得
                name, ext = os.path.splitext(abspath)
                # .wavの場合だけ追加
                if ext == '.wav':
                    self.myListView.addItem({u"name": file})

                print 'This is not Dir :', abspath

# =============================================================================
## GUIの起動
def main():
    app = QApplication(sys.argv)
    wnd = GUI()
    wnd.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
