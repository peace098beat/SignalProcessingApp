# EXAMPLES Houdini 13

################################# Simple widget
# import hqt
import hqt
# import my module with widget class
import myWidget
# just send widget class to hqt to open
hqt.showUi(myWidget.windowClass)


################################# Modified widget
# If you need to modify widget before show or send arguments to creator
# you need to get QApplication before create widget manualy
#import hqt
import hqt
# import my module with widget class
import myWidget
# get application
app = hqt.application()
# create my widget with arguments
args = [1,2,3]
window = myWidget.windowClass(args)
# modify after create
window.move(10,20)
# send to hqt to show
hqt.showUi(window, app)

################################# Communicate Widget
# hqt.showUi return widget object. You can use it after open.

import hqt
class myWidget(hqt.QWidget):
    def __init__(self):
        super(myWidget, self).__init__()
w = hqt.showUi(myWidget)
# exec some methods or modify widget
# Window already opened
w.someMethod()
w.resize(100,200)

################################# Dialog
import hqt
class myDialog(hqt.QDialog):
    def __init__(self):
        super(myDialog, self).__init__(None)
        self.setWindowTitle('Test Dialog')
        self.resize(200,200)

result, dialog = hqt.showUi(myDialog)
if result:
    #read some data from dialog
    pass

################################# Menu
# Open menu in current cursor pos

import hqt
class myMenu(hqt.QMenu):
    def __init__(self):
        super(myMenu, self).__init__()
        for i in range(10):
            self.addAction(hqt.QAction('Item %s' % i, self))

action = hqt.showUi(myMenu)
# get data from action object
print action.text()


######################################################################################## 14

# EXAMPLES HOUDINI 14

########## Simple Window
import myWidget
import hqt
w = myWidget()
w.setParent(hqt.getHouWindow())
w.setStyleSheet(hqt.get_h14_style())
w.show()

######## Insert as Panel
import hqt
#1
import myWidget
# in panel
hqt.show(myWidget.mainWindow, name='My Widget',replacePyPanel=1, hideTitleMenu=0)
# floating
hqt.show(myWidget.mainWindow, floating=1, position=(200,300), size=(300,400))

