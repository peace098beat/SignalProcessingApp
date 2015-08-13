import sys
from PyQt4 import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")

        self.file_menu = self.menuBar().addMenu('&File')
        self.file_menu.addAction('New...', self.newFile)
        self.file_menu.addAction('Open...', self.openFile)
        self.file_menu.addAction('Quit...', QtGui.qApp.quit)

        self.t = QtGui.QToolBar(self)
        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('exit'), 'Exit',self)
        self.t.addAction(exitAction)
        icon = QtGui.QIcon('tmp1.png')
        self.t.addAction(icon, 'New File', self.newFile)
        icon = QtGui.QIcon('tmp2.png')
        self.t.addAction(icon, 'Open File', self.openFile)
        icon = QtGui.QIcon('tmp3.png')
        self.t.addAction(icon, 'Quit', QtGui.qApp.quit)
        self.addToolBar(self.t)

        self.te = QtGui.QTextEdit()
        self.setCentralWidget(self.te)

        self.le1 = QtGui.QLineEdit()
        self.top_dock = QtGui.QDockWidget("File Name", self)
        self.top_dock.setWidget(self.le1)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.top_dock)

        label = QtGui.QLabel()
        label.setText('Size')
        self.sl = QtGui.QLabel()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.sl)
        widget = QtGui.QWidget()
        widget.setLayout(hbox)
        self.left_dock = QtGui.QDockWidget("File Info", self)
        self.left_dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.left_dock)

        self.status_bar = QtGui.QStatusBar(self)
        self.status_bar.showMessage('Here is Status Bar', 5000)
        self.setStatusBar(self.status_bar)


    def newFile(self):
        self.te.setText('')
        self.le.setText('')
        self.status_bar.showMessage('New File', 5000)


    def openFile(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/User/abe')
        fp = open(fn)
        data = fp.read()
        self.te.setText(data)
        fp.close()
        self.le1.setText(fn)
        l = len(data)
        self.sl.setText(str(l))
        self.status_bar.showMessage('Open File ' + fn, 5000)


app = QtGui.QApplication(sys.argv)
m = MainWindow()
m.show()
sys.exit(app.exec_())