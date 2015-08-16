#! coding:utf-8
"""
DraggableLine.py

MatplotlibのFigure上で、オブジェクトをD&Dで動かすための関数

使い方

fig,ax = plt.subplot()
lines, = ax.plot(X)

# ラインにイベントをコネクトして格納しておく
dls = []
for line in lines:
    dl = DraggableLine(line)
    dl.connect()
    dls.append(dl)


"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class DraggableLine:
    lock = None  # Only one can be animated at a time

    def __init__(self, line):
        self.line = line
        self.press = None
        self.background = None

    def connect(self):
        """connect to all the events we needs"""
        self.cidpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        # クリックがaxes内かを保障
        if event.inaxes is not self.line.axes:
            return
        # アニメーション可能かチェック
        # ロックされていればreturn
        if DraggableLine.lock is not None:
            return

        contains, attrd = self.line.contains(event)
        if not contains:
            return

        # マウスがクリックされた時の, rectの位置 (左下)
        x0, x1 = self.line.get_xdata()
        y0, y1 = self.line.get_ydata()

        # マウスがクリックされた時の, マウス座標も格納
        self.press = x0, y0, x1, y1, event.xdata, event.ydata


        # #######################################
        # アニメーション
        # #######################################
        DraggableLine.lock = self
        # ハンドラの取得
        canvas = self.line.figure.canvas
        axes = self.line.axes
        # アニメーションのセット
        self.line.set_animated(True)
        canvas.draw()
        # 背景のセット
        self.background = canvas.copy_from_bbox(self.line.axes.bbox)
        # rectだけを再描画 (now redraw just the rectangle)
        axes.draw_artist(self.line)
        # 移動したとこだけ再描画? (and blit just the redrawn area)
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        """ マウスの動きを常に監視 """
        # アニメーションフラグ
        if DraggableLine.lock is not self:
            return
        # マウス押下のフラグ
        # if self.press is None:
        #     return
        # 座標値内を保障
        if event.inaxes is not self.line.axes:
            return

        # x0, y0、移動前のrectの基準座標 (左下)
        # xpress, ypress、移動前のマウス座標
        x0, y0, x1, y1, xpress, ypress = self.press
        # 移動前のマウス座標と、現在のマウス座標から移動距離を算出
        # dx = event.xdata - xpress
        dy = event.ydata - ypress
        # print 'x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' % (x0, xpress, event.xdata, dx, x0+dx)
        # rectに移動距離分の座標値を加算
        # self.line.set_x(x0+dx)
        self.line.set_ydata([y0 + dy, y1 + dy])


        # #######################################
        # アニメーション
        # #######################################
        # ハンドラの取得
        canvas = self.line.figure.canvas
        axes = self.line.axes
        # restore the background region
        canvas.restore_region(self.background)
        # redraw just the current rectangel
        axes.draw_artist(self.line)
        # blit just the redrawn area
        canvas.blit(axes.bbox)

        # 再描画
        # self.rect.figure.canvas.draw()

    def on_release(self, event):
        if DraggableLine.lock is not self:
            return
        self.press = None

        # #######################################
        # アニメーション
        # #######################################
        DraggableLine.lock = None
        self.line.set_animated(False)
        self.background = None

        # 再描画
        self.line.figure.canvas.draw()



# データの生成
Nx = 1000
X = np.random.randn(Nx)*100

#########################################
# handles
#########################################
fig = plt.figure(figsize=(10,2), dpi=72, facecolor=[1,1,1], edgecolor=[0,0,0], linewidth=1.0, frameon=False,  tight_layout=False)

ax1 = plt.subplot2grid( (1,9), (0,0), colspan=8)
ax2 = plt.subplot2grid( (1,9), (0,8))

# ax2.axis('off')
ax1.grid()
ax2.set_xticklabels([])
ax2.set_yticklabels([])

#########################################
# axes 1
#########################################
lines, = ax1.plot(X)

#########################################
# axes 2
#########################################
n, bins, patches = ax2.hist(x=X, bins=100, orientation='horizontal', histtype='step')
# histtype :
#   {'bar', 'barstacked', 'step',  'stepfilled'}
# ax2のlimを取得
ax2.xmin, ax2.xmax = ax2.get_xlim()
ax2.ymin, ax2.ymax = ax2.get_ylim()
# ax1とax2の上限を一致させる
ax1.set_ylim(ax2.get_ylim())

# スケールを定めるためのラインを、ヒストグラム上に表示する
line_means, = ax2.plot([ax2.xmin, ax2.xmax], [X.mean(), X.mean()])
line_upper, = ax2.plot([ax2.xmin, ax2.xmax], [3 * X.std(), 3 * X.std()])
line_lower, = ax2.plot([ax2.xmin, ax2.xmax], [-3 * X.std(), -3 * X.std()])
# ラインをまとめる
ax2lines = [line_upper, line_lower]
# ラインにイベントをコネクトして格納しておく
dls = []
for line in ax2lines:
    dl = DraggableLine(line)
    dl.connect()
    dls.append(dl)

#########################################
# イベント
#########################################
def line_upper_draw_event(event):
    print 'line_upper_draw_event'
    [ymin, a] = ax1.get_ylim()
    a, ymax = line_upper.get_ydata()
    ax1.set_ylim([ymin, ymax])

def line_lower_draw_event(event):
    print 'line_lower_draw_event'
    [a, ymax] = ax1.get_ylim()
    ymin, a = line_lower.get_ydata()
    ax1.set_ylim([ymin, ymax])

#########################################
# コネクト
#########################################
line_upper.figure.canvas.mpl_connect('motion_notify_event', line_upper_draw_event)
line_lower.figure.canvas.mpl_connect('motion_notify_event', line_lower_draw_event)


# --
plt.show()

fig.savefig('graph_limit_selector.png')
