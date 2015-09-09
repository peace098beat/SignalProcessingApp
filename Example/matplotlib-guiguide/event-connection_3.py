#! coding:utf-8

import numpy as np
import matplotlib.pyplot as plt


class DraggableRectangle:

    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        """connect to all the events we needs"""
        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):

        # クリックがaxes内かを保障
        if event.inaxes is not self.rect.axes:
            return

        contains, attrd = self.rect.contains(event)
        # print contains, attrd

        if not contains:
            print 'not contains'
            return

        print 'event contains', self.rect.xy

        # マウスがクリックされた時の, rectの位置 (左下)
        x0, y0 = self.rect.xy
        # マウスがクリックされた時の, マウス座標も格納
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self,event):
        """ マウスの動きを常に監視 """

        # マウス押下のフラグ
        if self.press is None:
            return
        # 座標値内を保障
        if event.inaxes is not self.rect.axes:
            return

        # x0, y0、移動前のrectの基準座標 (左下)
        # xpress, ypress、移動前のマウス座標
        x0, y0, xpress, ypress = self.press

        # 移動前のマウス座標と、現在のマウス座標から移動距離を算出
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        print 'x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' % (x0, xpress, event.xdata, dx, x0+dx)

        # rectに移動距離分の座標値を加算
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        # 再描画
        self.rect.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.rect.figure.canvas.draw()








if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects = ax.bar(range(10), 20*np.random.rand(10))
    drs = []
    for rect in rects:
        dr = DraggableRectangle(rect)
        dr.connect()
        drs.append(dr)
    plt.show()
