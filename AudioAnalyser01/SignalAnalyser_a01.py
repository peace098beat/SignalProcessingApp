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
from UI_SignalAnalyser_a01 import Ui_MainWindow

## FiSigモジュール
from FiSig.AudioManager import AudioManager

## uiファイル名
uiFile = 'UI_SignalAnalyser_a01.ui'

## グローバル変数
audio_manager = AudioManager()


# =============================================================================
## GUIの構築
class GUI(MasterOfMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        MasterOfMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

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
        # Event の接続
        # ====================================
        self.fileloaded.connect(self.flashStatusBar)
        self.fileloaded.connect(self._subroutin)

    # ==========================================
    # Slotの設定
    # ==========================================
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
        if len(data) >= fs / 2:
            data = data[0:fs / 2 - 1]
        N = len(data)

        # --- データを格納 ---
        self.wave_d = data
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
        d_gwt = 20 * np.log10(np.abs(d_gwt))
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
        self.figure1.plot(ydata=self.wave_d)
        self.figure2.plot(zdata=self.gwt_d, extent=self.gwt_extent)

        pass

    @Slot()
    def _subroutin(self):
        self.analys()
        self.plot()


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
