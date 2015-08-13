#! encoding:utf-8
"""
MasterOfMainWindow.py

使い方

ステータスバー
self.statusBar().showMessage("File saved", 2000)

"""
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *


class MasterOfMainWindow(QMainWindow):
    """ Our Main Window Class
    """
    def __init__(self):
        QMainWindow.__init__(self)
        # MainWindowの基本設定
        self.setWindowTitle("Main Window")
        self.setGeometry(300, 250, 400, 300)
        self.setWindowIcon(QIcon('./FiSig/icon/icon_fifi.png'))

        # メンバ変数の定義
        self.fileName = None

        # メニューバーと、ステータスバーの生成
        self.setupComponents()

        # UIの生成
        # self.setupUI()

    def setupUI(self):
        # メインバーの生成

        # 子ウィジェットの生成
        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        # 子ウィジェットの生成
        self.amtLabel = QLabel('Loan Amount')
        self.roiLabel = QLabel('Rate of Interest')
        self.yrsLabel = QLabel('No. of Years')
        self.emiLabel = QLabel('EMI per month')
        self.emiValue = QLCDNumber()
        # ----
        self.emiValue.setSegmentStyle(QLCDNumber.Flat)
        self.emiValue.setFixedSize(QSize(130, 30))
        self.emiValue.setDigitCount(8)
        # ----
        self.amtText = QLineEdit('10000')
        # ----
        self.roiSpin = QSpinBox()
        self.roiSpin.setMinimum(1)
        self.roiSpin.setMaximum(15)
        # ----
        self.yrsSpin = QSpinBox()
        self.yrsSpin.setMinimum(1)
        self.yrsSpin.setMaximum(20)
        # ----
        self.roiDial = QDial()
        self.roiDial.setNotchesVisible(True)
        self.roiDial.setMinimum(1)
        self.roiDial.setMaximum(15)
        self.roiDial.setValue(1)
        # ----
        self.yrsSlide = QSlider(Qt.Horizontal)
        self.yrsSlide.setMaximum(20)
        self.yrsSlide.setMinimum(1)
        # ----
        self.calculateBuutton = QPushButton('Calculate EMI')
        # ----
        self.myGridLayout = QGridLayout(self.widget)
        # ----
        self.myGridLayout.addWidget(self.amtLabel, 0, 0)
        self.myGridLayout.addWidget(self.roiLabel, 1, 0)
        self.myGridLayout.addWidget(self.yrsLabel, 2, 0)
        self.myGridLayout.addWidget(self.amtText, 0, 1)
        self.myGridLayout.addWidget(self.roiSpin, 1, 1)
        self.myGridLayout.addWidget(self.yrsSpin, 2, 1)
        self.myGridLayout.addWidget(self.roiDial, 1, 2)
        self.myGridLayout.addWidget(self.yrsSlide, 2, 2)
        self.myGridLayout.addWidget(self.calculateBuutton, 3, 0, 1, 3)
        self.myGridLayout.addWidget(self.emiLabel, 4, 1)
        self.myGridLayout.addWidget(self.emiValue, 4, 2)

        # ----
        # Connect SIGNAL & SLOT
        self.roiDial.valueChanged.connect(self.roiSpin.setValue)
        self.roiSpin.valueChanged.connect(self.roiDial.setValue)

        self.connect(self.roiDial, SIGNAL("valueChanged(int)"), self.roiSpin.setValue)
        self.connect(self.roiSpin, SIGNAL("valueChanged(int)"), self.roiDial.setValue)

        self.yrsSlide.valueChanged.connect(self.yrsSpin.setValue)
        self.yrsSpin.valueChanged.connect(self.yrsSlide.setValue)

        self.connect(self.calculateBuutton, SIGNAL("clicked()"), self.showEMI)
        self.calculateBuutton.clicked.connect(self.showEMI)

        self.roiDial.valueChanged.connect(self.showEMI)
        self.roiSpin.valueChanged.connect(self.showEMI)
        self.yrsSlide.valueChanged.connect(self.showEMI)
        self.yrsSpin.valueChanged.connect(self.showEMI)

    def showEMI(self):
        loanAmount = float(self.amtText.text())
        rateInterest = float(float(self.roiSpin.value() / 12.0) / 100.0)
        noMonths = int(self.yrsSpin.value() * 12)
        c = (1+rateInterest) ** noMonths
        emi = (loanAmount * rateInterest) * c/(c-1)
        # ---
        self.emiValue.display(emi)

    #
    # ==================================================================
    # メインバーの作成
    # ==================================================================
    def setupComponents(self):
        """ 各バーの生成 """
        # ステータスバーの生成
        self.createStatusBar()
        # アクションの生成
        self.createActions()
        # メニューバーの生成
        self.createMenusBar()
        # ツールバーの生成
        self.createToolBar()

    def createStatusBar(self):
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage('Ready', 10000)

    def createActions(self):
        self.openAction = QAction( QIcon('./FiSig/icon/png/share-boxed-2x.png'), 'Open', self,
                                   shortcut = QKeySequence.Open,
                                   statusTip= 'Open an existing file',
                                   triggered=self.openFile)

        self.saveAction = QAction( QIcon('./FiSig//icon/png/task-2x.png'), 'Save', self,
                                   shortcut = QKeySequence.Save,
                                   statusTip= 'Save file',
                                   triggered=self.saveFile)

        self.exitAction = QAction( QIcon('./FiSig//icon/png/power-standby-2x.png'), 'E&xit', self,
                                   shortcut="Ctrl+Q",
                                   statusTip="Exit the Application",
                                   triggered=self.exitFile)

        self.aboutAction = QAction( QIcon('./FiSig/icon/png/print-2x.png'), 'A&bout', self,
                                    statusTip="Displays info about text editor",
                                    triggered=self.aboutHelp)

    def createToolBar(self):
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.openAction)
        self.mainToolBar.addAction(self.saveAction)
        self.mainToolBar.addSeparator()

    def createMenusBar(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.helpMenu = self.menuBar().addMenu("&Help")
        # MenuへQActionたちを生成
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        # ------
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addSeparator()
        # ------

    # ==================================================================
    # シグナル用の動作関数
    # ==================================================================
    def openFile(self):
        self.fileName, self.filterName = QFileDialog.getOpenFileName(self)
        self.statusBar().showMessage("File opened"+self.fileName, 2000)

    def saveFile(self):
        self.statusBar().showMessage("File saved", 2000)

    def exitFile(self):
        self.close()

    def aboutHelp(self):
        QMessageBox.about(self, "About Simple Text Editor",
                          "This example demonstrates the use of Menu Bar")

    def openFileDialog(self):
        fname, filt = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Wave Files (*.wav);; All Files (*)')
        print 'openFileDialog loadfile', str(fname)


    # ==================================================================
    # イベント処理
    # ==================================================================
    def dragEnterEvent(self, event):
        """ドラッグイベントの検知
        """
        print 'dragEnterEvent'
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """ドロップイベントの検知
        """
        print 'dropEvent'
        files = [unicode(u.toLocalFile()) for u in event.mimeData().urls()]
        for fname in files:
            print type(fname)
            print 'dropEvent', str(fname)


if __name__ == '__main__':
    # Exception Handling
    try:
        myApp = QApplication(sys.argv)
        mainWindow = MasterOfMainWindow()
        mainWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
