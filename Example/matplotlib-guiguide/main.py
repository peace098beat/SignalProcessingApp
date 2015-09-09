import pylab as pl
import numpy as np

import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.color'] = 'b'


X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)


pl.figure(figsize=(10, 6), dpi=80, edgecolor=[0,0,0])
pl.plot(X, C, color="blue")
pl.plot(X, S, color="red")
# pl.xlim(X.min() * 1.1, X.max() * 1.1)
# pl.ylim(C.min() * 1.1, C.max() * 1.1)

ax = pl.gca()  # gca stands for 'get current axis'
# ax.set_xlim(0, 4)
# ax.set_ylim(0, 3)


ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',-3))
ax.spines['left'].set_color('none')

ax.spines['bottom'].set_position(('data',-1.0))
ax.spines['bottom'].set_color('none')
ax.xaxis.set_ticks_position('bottom')




# Show result on screen
pl.show()