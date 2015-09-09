import numpy as np
from scipy.signal import freqs, iirfilter, iirdesign

wp = [0.2, 0.5]
ws = [0.1, 0.6]
gpass = 1
gstop = 20
b, a = iirdesign(wp,ws,gpass,gstop,analog=True,ftype='cheby1')
# print b, a

N = 4 # order
Wn = [1, 10] # freq
rp = 1 # ripple[db]
rs = 60 # stopband gain [db]
# b, a = iirfilter(4, [1, 10], 1, 60, analog=True, ftype='cheby1')
b, a = iirfilter(N, Wn,rp,rs,btype='bandpass', analog=False, ftype='cheby1')

import matplotlib.pyplot as plt
w, h = freqs(b, a, worN=np.logspace(-1, 2, 1000))

# plt.semilogx(w, 20 * np.log10(np.imag(h)))
plt.semilogx(w, np.imag(h))
plt.xlabel('Frequency')
plt.ylabel('Amplitude response [dB]')
# plt.ylim(-120,5)
plt.grid()
plt.show()

# w, h = freqs(b, a)

# plt.plot(w, 20 * np.log10(abs(h)))
# plt.xlabel('Frequency')
# plt.ylabel('Amplitude response [dB]')
# plt.ylim(-120,10)
# plt.xlim(0,1)
# plt.grid()
# plt.show()
