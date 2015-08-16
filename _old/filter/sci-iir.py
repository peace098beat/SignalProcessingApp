#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scipy as sp
import scipy.signal as sig
import wave

fsamp = 44100.0
fpass = 5000.0
fstop = 6000.0
wp = fpass / (fsamp / 2 )
ws = fstop / (fsamp / 2 )
b,a = sig.iirdesign(wp, ws, 1, 30)
fs, h = sig.freqs(b,a)

filename='white_noise2.wav'
wf = wave.open(filename,'rb')
n=wf.getnframes()
s=wf.readframes(n)
x = sp.fromstring(s,sp.int16)
y = sig.lfilter(b,a,x)

o_filename='filtered.wav'
wf_o=wave.open(o_filename,'wb')
wf_o.setnchannels(1)
wf_o.setsampwidth(2)
wf_o.setframerate(44100)
wf_o.writeframes(sp.int16(y).tostring())
wf_o.close()
wf.close()