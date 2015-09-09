# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qss13.ui'
#
# Created: Sun Aug 23 21:44:21 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(646, 467)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("/*fisig_stylesheet_a1.css*/\n"
"\n"
"/******* QWidget ********/\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color:#3a3a3a;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #252525;\n"
"}\n"
"\n"
"QAbstractScrollArea,QTableView\n"
"{\n"
" border: 1px solid #222;\n"
"}\n"
"\n"
"\n"
"/************** QMainWindow *************/\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 2px; \n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; \n"
"}\n"
"\n"
"\n"
"/************** QToolTip **************/\n"
"\n"
"QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #000;\n"
"     padding: 1px;\n"
"     padding-left: 4px;\n"
"     padding-right: 4px;\n"
"     border-radius: 3px;\n"
"     color: white;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"\n"
"/***************** QMenuBar *************/\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background-color: #555555;\n"
"    color: #fff;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"\n"
"/**************** QMenu **********/\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    background-color: #3a3a3a;\n"
"    padding: 2px 20px 2px 20px;\n"
"    margin-left: 14px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #fff;\n"
"    background-color: #555555;\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 20px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"\n"
"/************* QAbstractItemView ***********/\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: #353535;\n"
"    alternate-background-color: #323232;\n"
"    outline: 0;\n"
"    height: 20px;\n"
"}\n"
"\n"
"\n"
"/************ QTreeView **********/\n"
"\n"
"QTreeView::item:alternate,\n"
"QListView::item:alternate  {\n"
"     background-color: #323232;\n"
" }\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item\n"
"{\n"
"    border-image: url(:/vline.png) 0;\n"
"}\n"
"QTreeView::branch:has-siblings:adjoins-item\n"
"{\n"
"    border-image: url(:/more.png) 0;\n"
"}\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item\n"
"{\n"
"    border-image: url(:/end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:closed:has-children:has-siblings\n"
"{\n"
"    border-image: url(:/closed.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:closed:has-children:!has-siblings\n"
"{\n"
"    border-image: url(:/closed_end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings\n"
"{\n"
"    border-image: url(:/open_end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:has-siblings\n"
"{\n"
"    border-image: url(:/open.png) 0;\n"
"}\n"
"\n"
"/********************* QListView ************/\n"
"\n"
"QListView::item,\n"
"QTreeView::item \n"
"{\n"
"    color: rgb(220,220,220);\n"
"    border-color: rgba(0,0,0,0);\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"}\n"
"\n"
"QListView::item:selected,\n"
"QTreeView::item:selected\n"
"{\n"
"    background: #605132;\n"
"    border-color: #b98620;\n"
" }\n"
"\n"
"/*************** QTableView ********/\n"
"\n"
"QHeaderView::section\n"
"{\n"
"   background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #393939, stop: 1 #272727);\n"
"   color: #b1b1b1;\n"
"   border: 1px solid #191919;\n"
"   border-top-width: 0px;\n"
"   border-left-width: 0px;\n"
"   padding-left: 10px;\n"
"   padding-right: 10px;\n"
"   padding-top: 3px;\n"
"   padding-bottom: 3px;\n"
"\n"
"}\n"
"QTableView {\n"
"    alternate-background-color: #2e2e2e\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background: #605132;\n"
"    border: 1px solid #b98620;\n"
"\n"
"    color: rgb(220,220,220);\n"
" }\n"
"\n"
"  QTableView QTableCornerButton::section {\n"
"     background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #393939, stop: 1 #272727);\n"
"     border: 1px solid #191919;\n"
"     border-top-width: 0px;\n"
"     border-left-width: 0px;\n"
" }\n"
"\n"
"\n"
"/*************** QlineEdit ************/\n"
"\n"
"QLineEdit,QDateEdit,QDateTimeEdit,QSpinBox\n"
"{\n"
"    background-color: #000;\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 2px solid #2b2b2b;\n"
"    border-radius: 0;\n"
"    color:rgb(255,255,255);\n"
"    min-height: 18px;\n"
"    selection-background-color: rgb(185,134,32);\n"
"    selection-color: rgb(0,0,0);\n"
"}\n"
"\n"
"\n"
"/*************** QPushButton ***********/\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"    border: 2px solid #232323;\n"
"    border-top-width: 2px;\n"
"    border-left-width: 2px;\n"
"    border-top-color:  QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #101010, stop: 1 #818181);\n"
"    border-left-color:  QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #101010, stop: 1 #818181);\n"
"    border-radius: 0;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"    background-color:   #424242;\n"
"    border: 2px solid #313131;\n"
"    border-top-width: 2px;\n"
"    border-left-width: 2px;\n"
"    border-top-color:  QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #151515, stop: 1 #777777);\n"
"    border-left-color:  QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #151515, stop: 1 #777777);\n"
"    color: #777;\n"
"}\n"
"\n"
"QPushButton:checked\n"
"{   \n"
"    border-color: #000;\n"
"    background-color: #2d2d2d;\n"
"    color: #cacaca;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
" QPushButton:hover\n"
"{   \n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #606060, stop: 0.1 #585858, stop: 0.5 #545454, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: #af8021;\n"
"    color: #fff;\n"
"}\n"
"\n"
"\n"
"/*********** QScrollBar ***************/\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: #222;\n"
"     height: 15px;\n"
"     margin: 0px 14px 0 14px;\n"
"}\n"
"QScrollBar:vertical\n"
"{\n"
"      border: 1px solid #222222;\n"
"      background: #222;\n"
"      width: 15px;\n"
"      margin: 14px 0 14px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"    background:  QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"    min-height: 20px;\n"
"    border-radius: 0px;\n"
"    border: 1px solid #222222;\n"
"    border-left-width: 0px;\n"
"    border-right-width: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background:  QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"    min-height: 20px;\n"
"    border-radius: 0px;\n"
"    border: 1px solid #222222;\n"
"    border-top-width: 0px;\n"
"    border-bottom-width: 0px;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal \n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 0px;\n"
"      background:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"      width: 14px;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 1px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"      height: 14px;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed ,\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::sub-line:vertical:pressed\n"
"{\n"
"      background:  #5b5a5a;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      subcontrol-position: top;\n"
"}\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      subcontrol-position: bottom;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal \n"
"{\n"
"     subcontrol-position: left;\n"
"}\n"
"QScrollBar::add-line:horizontal\n"
"{\n"
"      subcontrol-position: right;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical\n"
"{\n"
"     border-image: url(:/arrow_up.png) 1;\n"
"}\n"
"QScrollBar::down-arrow:vertical\n"
"{\n"
"     border-image: url(:/arrow_down.png) 1;\n"
"}\n"
"QScrollBar::right-arrow:horizontal\n"
"{\n"
"     border-image: url(:/arrow_right.png) 1;\n"
"}\n"
"QScrollBar::left-arrow:horizontal\n"
"{\n"
"     border-image: url(:/arrow_left.png) 1;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"/********* QSlider **************/\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #000;\n"
"    background: #000;\n"
"    height: 3px;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background:  #404040;\n"
"    border: 1px solid #000;\n"
"    height: 10px;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #626262;\n"
"    border: 1px solid #000;\n"
"    height: 10px;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,   stop:0 #696969, stop:1 #505050);\n"
"border: 1px solid #000;\n"
"width: 5px;\n"
"margin-top: -8px;\n"
"margin-bottom: -8px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QSlider::hover\n"
"{\n"
"    background: #3f3f3f;    \n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"border: 1px solid #ffaa00;\n"
"background: #ffaa00;\n"
"width: 3px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:vertical {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,   stop: 0 #ffaa00, stop: 1 #ffaa00);\n"
"background:#404040;\n"
"border: 1px solid #000;\n"
"width: 8px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"QSlider::sub-page:vertical {\n"
"background: #626262;\n"
"border: 1px solid #000;\n"
"width: 8px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:vertical {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,   stop:0 #696969, stop:1 #505050);\n"
"border: 1px solid #000;\n"
"height: 5px;\n"
"margin-left: -8px;\n"
"margin-right: -8px;\n"
"border-radius: 0px;\n"
"}\n"
"\n"
"/* disabled */\n"
"\n"
"QSlider::sub-page:disabled, QSlider::add-page:disabled \n"
"{\n"
"border-color: #3a3a3a;\n"
"background: #414141;\n"
"border-radius: 0px;\n"
"}\n"
"QSlider::handle:disabled {\n"
"background: #3a3a3a;\n"
"border: 1px solid #242424;\n"
"\n"
"}\n"
"\n"
"QSlider::disabled {\n"
"background: #3a3a3a;\n"
"}\n"
"\n"
"\n"
"/********* QProgressBar ***********/\n"
"QProgressBar\n"
"{\n"
"    border: 1px solid #6d6c6c;\n"
"    border-radius: 0px;\n"
"    \n"
"    text-align: center;\n"
"    background:#262626;\n"
"    color: gray;\n"
"    border-bottom: 1px #545353;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, \n"
"    stop: 0 #f0d66e,\n"
"    stop: 0.09 #f0d66e,\n"
"    stop: 0.1 #ecdfa8, \n"
"    stop: 0.7 #d9a933, \n"
"    stop: 0.91 #b88822);\n"
"\n"
"}\n"
"\n"
"\n"
"/************ QComboBox ************/\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #515151,  stop: 0.5 #484848, stop: 1 #3d3d3d);\n"
"    border-style: solid;\n"
"    border: 1px solid #000;\n"
"    border-radius: 0;\n"
"    padding-left: 9px;\n"
"    min-height: 20px;\n"
"    font: 10pt;\n"
"\n"
"}\n"
"\n"
"QComboBox:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #555555,  stop: 0.5 #4d4d4d, stop: 1 #414141);\n"
"   /* font: 14pt;*/\n"
"}\n"
"\n"
"QComboBox:on\n"
"{\n"
"    background-color: #b98620;\n"
"    color:#fff;\n"
"    selection-background-color: #494949;\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 25px;\n"
"     background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #3d3d3d,  stop: 1 #282828);\n"
"     border-width: 0px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"    image: url(:/arrow_up_down.png);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    background-color: #3a3a3a;\n"
"    border-radius: 0px;\n"
"    border: 1px solid #101010;\n"
"    border-top-color:  #818181;\n"
"    border-left-color: #818181;\n"
"    selection-background-color: #606060;\n"
"    padding: 2px;\n"
"\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item \n"
"{\n"
"    margin-top: 3px;\n"
"}\n"
"\n"
"QListView#comboListView {\n"
"    background: rgb(80, 80, 80);\n"
"    color: rgb(220, 220, 220);\n"
"    min-height: 90px;\n"
"    margin: 0 0 0 0;\n"
"}\n"
"\n"
"QListView#comboListView::item {\n"
"    background-color: rgb(80, 80, 80);\n"
"}\n"
"\n"
"QListView#comboListView::item:hover {\n"
"    background-color: rgb(95, 95, 95);\n"
"}\n"
"\n"
"\n"
"\n"
"/************ QCheckBox *********/\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background:black;\n"
"    image: url(:/cb_unchecked_d.png);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(:/cb_checked_d.png);\n"
"}\n"
"QCheckBox::indicator:unchecked:disabled {\n"
"    background:black;\n"
"    image: url(:/cb_unchecked_dis_d.png);\n"
"}\n"
"QCheckBox::indicator:checked:disabled {\n"
"    image: url(:/cb_checked_dis_d.png);\n"
"}\n"
"\n"
"\n"
"/****** QRadioButton ***********/\n"
"\n"
"QRadioButton::indicator:unchecked \n"
"{\n"
"    image: url(:/rb_unchecked_d.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked \n"
"{\n"
"    image: url(:/rb_checked_d.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:disabled\n"
"{\n"
"    image: url(:/rb_unchecked_dis_d.png);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled\n"
"{\n"
"    image: url(:/rb_checked_dis_d.png);\n"
"}\n"
"\n"
"\n"
"/****** QTabWidget *************/\n"
"\n"
"\n"
"QTabWidget::pane  { \n"
"    border: 1px solid #111111;\n"
"    margin-top:-1px; /* hide line under selected tab*/\n"
"\n"
"}\n"
"\n"
"QTabWidget::tab-bar  {\n"
"    left: 0px; /* move to the right by 5px */\n"
"}\n"
" \n"
"QTabBar::tab  {\n"
"    border: 1px solid #111;\n"
"    border-radius: 0px;\n"
"    min-width: 15ex;\n"
"    padding-left: 3px;\n"
"    padding-right: 5px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #313131,  stop: 1 #252525);\n"
"     \n"
"}\n"
"\n"
"QTabBar::tab:selected  {\n"
"    border-bottom: 0px;\n"
"    background-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4b4b4b,  stop: 1 #3a3a3a)\n"
"}\n"
"\n"
" \n"
"QTabBar::tab:only-one  {\n"
"    margin: 0;\n"
"}\n"
"\n"
"\n"
"\n"
"/************** QGroupBox *************/\n"
" QGroupBox {\n"
"    border-left-color:QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #4b4b4b,  stop: 1 #3a3a3a);\n"
"    border-right-color:QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #111,  stop: 1 #3a3a3a);\n"
"    border-top-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2:1, stop: 0 #4b4b4b,  stop: 1 #3a3a3a);\n"
"    border-bottom-color:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #111,  stop: 1 #3a3a3a);\n"
"    border-width: 2px; \n"
"    border-style: solid; \n"
"    border-radius: 0px;\n"
"    padding-top: 10px;\n"
"}\n"
"QGroupBox::title { \n"
"    background-color: transparent;\n"
"     subcontrol-position: top left;\n"
"     padding:4 10px;\n"
" } \n"
"\n"
"\n"
"/************************ QSpinBox *******************/\n"
"/*,QDoubleSpinBox*/\n"
"\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button, QTimeEdit::up-button  {\n"
"    /*background:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 1 #3a3a3a);*/\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 16px;\n"
"    /*border: 1px solid #333;*/\n"
"} \n"
"QSpinBox::down-button, QDoubleSpinBox::down-button,  QTimeEdit::down-button{\n"
"   /* background:QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 1 #3a3a3a);*/\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 16px;\n"
"   /* border: 1px solid #333;*/\n"
"}\n"
"\n"
"QSpinBox::down-button,QDoubleSpinBox::down-button,  QTimeEdit::down-button,\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button,QTimeEdit::up-button \n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #535353, stop: 0.1 #515151, stop: 0.5 #474747, stop: 0.9 #3d3d3d, stop: 1 #3a3a3a);\n"
"    border: 2px solid #232323;\n"
"    border-top-width: 2px;\n"
"    border-left-width: 2px;\n"
"    border-top-color:  QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #101010, stop: 1 #818181);\n"
"    border-left-color:  QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #101010, stop: 1 #818181);\n"
"    border-radius: 0;\n"
"\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed, QSpinBox::down-button:pressed,\n"
"QTimeEdit::up-button:pressed ,QDoubleSpinBox::up-button:pressed , QTimeEdit::down-button:pressed \n"
"{\n"
"    background-color: #828282;\n"
"}\n"
"\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button  {\n"
"    image: url(:/spin_up.png);\n"
"}\n"
"\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button  {\n"
"    image: url(:/spin_down.png);\n"
"}\n"
"\n"
"\n"
"QPlainTextEdit, QTextEdit {\n"
"    background: #000;\n"
"    color: white;\n"
"}\n"
"QTextBrowser {\n"
"   background-color:#3a3a3a;\n"
"}\n"
"QTabBar::close-button {\n"
"     image: url(:/tab_close.png);\n"
"     subcontrol-position: right;\n"
" }\n"
"QTabBar::close-button:hover {\n"
"     image: url(:/tab_close_hover.png);\n"
" }")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtGui.QTabWidget.Triangular)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 35, 271, 176))
        self.groupBox.setStyleSheet("border-radius: 20px;")
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 25, 101, 23))
        self.pushButton.setCursor(QtCore.Qt.CrossCursor)
        self.pushButton.setMouseTracking(True)
        self.pushButton.setCheckable(True)
        self.pushButton.setAutoRepeat(True)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.toolButton = QtGui.QToolButton(self.groupBox)
        self.toolButton.setGeometry(QtCore.QRect(130, 30, 21, 18))
        self.toolButton.setObjectName("toolButton")
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(15, 65, 86, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(15, 95, 86, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(130, 65, 75, 16))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(130, 100, 75, 16))
        self.checkBox_2.setObjectName("checkBox_2")
        self.buttonBox = QtGui.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(100, 135, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.commandLinkButton = QtGui.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(420, 375, 185, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(45, 225, 271, 186))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.toolBox = QtGui.QToolBox(self.tab)
        self.toolBox.setGeometry(QtCore.QRect(15, 15, 69, 121))
        self.toolBox.setObjectName("toolBox")
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 67, 67))
        self.page.setObjectName("page")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 67, 67))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(115, 20, 50, 12))
        self.label.setObjectName("label")
        self.horizontalSlider = QtGui.QSlider(self.tab)
        self.horizontalSlider.setGeometry(QtCore.QRect(100, 40, 160, 19))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalScrollBar = QtGui.QScrollBar(self.tab)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(100, 65, 160, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.timeEdit = QtGui.QTimeEdit(self.tab)
        self.timeEdit.setGeometry(QtCore.QRect(110, 100, 118, 24))
        self.timeEdit.setObjectName("timeEdit")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(385, 75, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.fontComboBox = QtGui.QFontComboBox(self.centralwidget)
        self.fontComboBox.setGeometry(QtCore.QRect(335, 110, 185, 22))
        self.fontComboBox.setObjectName("fontComboBox")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(335, 155, 113, 24))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(335, 185, 221, 36))
        self.textEdit.setObjectName("textEdit")
        self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(335, 245, 104, 71))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(495, 10, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(335, 340, 221, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 646, 24))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtGui.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAdd = QtGui.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFIle.addAction(self.actionOpen)
        self.menuFIle.addAction(self.actionAdd)
        self.menuFIle.addAction(self.actionClose)
        self.menuFIle.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFIle.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>Button!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("MainWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("MainWindow", "CheckBox", None, QtGui.QApplication.UnicodeUTF8))
        self.commandLinkButton.setText(QtGui.QApplication.translate("MainWindow", "CommandLinkButton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QtGui.QApplication.translate("MainWindow", "Page 1", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("MainWindow", "Page 2", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "wave", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "fft", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "gwt", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "gwtdc", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFIle.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

