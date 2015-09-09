#! coding:utf-8

import numpy as np
import matplotlib.pyplot as plt


class DraggableRectangle:
    lock = None # Only one can be animated at a time

    def __init__(self, rect):
        self.rect = rect
        self.press = None
        self.background = None

    def connect(self):
        """connect to all the events we needs"""
        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        # クリックがaxes内かを保障
        if event.inaxes is not self.rect.axes:
            return
        # アニメーション可能かチェック
        # ロックされていればreturn
        if DraggableRectangle.lock is not None:
            return

        contains, attrd = self.rect.contains(event)
        # print contains, attrd

        if not contains:
            # print 'not contains'
            return

        # print 'event contains', self.rect.xy

        # マウスがクリックされた時の, rectの位置 (左下)
        x0, y0 = self.rect.xy
        # マウスがクリックされた時の, マウス座標も格納
        self.press = x0, y0, event.xdata, event.ydata


        # #######################################
        # アニメーション
        # #######################################
        DraggableRectangle.lock = self
        # ハンドラの取得
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # アニメーションのセット
        self.rect.set_animated(True)
        canvas.draw()
        # 背景のセット
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)
        # rectだけを再描画 (now redraw just the rectangle)
        axes.draw_artist(self.rect)
        # 移動したとこだけ再描画? (and blit just the redrawn area)
        canvas.blit(axes.bbox)

    def on_motion(self,event):
        """ マウスの動きを常に監視 """
        # アニメーションフラグ
        if DraggableRectangle.lock is not self:
            return
        # マウス押下のフラグ
        # if self.press is None:
        #     return
        # 座標値内を保障
        if event.inaxes is not self.rect.axes:
            return

        # x0, y0、移動前のrectの基準座標 (左下)
        # xpress, ypress、移動前のマウス座標
        x0, y0, xpress, ypress = self.press
        # 移動前のマウス座標と、現在のマウス座標から移動距離を算出
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print 'x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' % (x0, xpress, event.xdata, dx, x0+dx)
        # rectに移動距離分の座標値を加算
        self.rect.set_x(x0+dx)
        # self.rect.set_y(y0+dy)


        # #######################################
        # アニメーション
        # #######################################
        # ハンドラの取得
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)
        # redraw just the current rectangel
        axes.draw_artist(self.rect)
        # blit just the redrawn area
        canvas.blit(axes.bbox)

        # 再描画
        # self.rect.figure.canvas.draw()

    def on_release(self, event):
        if DraggableRectangle.lock is not self:
            return
        self.press = None

        # #######################################
        # アニメーション
        # #######################################
        DraggableRectangle.lock = None
        self.rect.set_animated(False)
        self.background = None

        # 再描画
        self.rect.figure.canvas.draw()








if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(10), 20*np.random.rand(10))
    rects = ax.bar(range(10), 20*np.random.rand(10))
    drs = []
    for rect in rects:
        dr = DraggableRectangle(rect)
        dr.connect()
        drs.append(dr)
    plt.show()
