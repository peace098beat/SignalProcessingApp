#! coding:utf-8
"""
Matplotlib_event_connections.py

http://matplotlib.org/users/event_handling.html


Event name	Class and description
‘button_press_event’	MouseEvent - mouse button is pressed
‘button_release_event’	MouseEvent - mouse button is released
‘draw_event’	DrawEvent - canvas draw
‘key_press_event’	KeyEvent - key is pressed
‘key_release_event’	KeyEvent - key is released
‘motion_notify_event’	MouseEvent - mouse motion
‘pick_event’	PickEvent - an object in the canvas is selected
‘resize_event’	ResizeEvent - figure canvas is resized
‘scroll_event’	MouseEvent - mouse scroll wheel is rolled
‘figure_enter_event’	LocationEvent - mouse enters a new figure
‘figure_leave_event’	LocationEvent - mouse leaves a figure
‘axes_enter_event’	LocationEvent - mouse enters a new axes
‘axes_leave_event’	LocationEvent - mouse leaves an axes

*MouseEvent*
http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.MouseEvent
bottom, left button pressed None, 1, 2, 3, ‘up’, ‘down’
event.button: (1,2,3) クリックされたボタンの判別
event.dblclick (bool)
event.inaxes ?
event.step ?
event.x: pixel値
event.xdata: プロットされているデータ上の位置(座標値)
event.y: pixel値
event.ydata: プロットされているデータ上の位置(座標値)

"""


import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
    if event.dblclick:
        print 'Double click'
    print event.inaxes
    print event.step

def ondraw(event):
    print 'canvas drawed'
    print event.name
    print event.canvas
    print event.guiEvent

# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# cid = fig.canvas.mpl_connect('button_release_event', onclick)
cid = fig.canvas.mpl_connect('draw_event', ondraw)


plt.show()