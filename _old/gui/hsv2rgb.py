# -*- coding: utf-8 -*-
import numpy as np


def hsv2rgb(H, S=1., V=1., A=1.):
    """HSV系からRGB空間へ変換2
    使い方：
        H: 0.0-240.0 (赤 - 青)
        S: 1.
        V: 1.
    Argument:
        h:  色相角度(0. - 240.)
        s:  彩度(0. - 1.)
        v:  明度(0. - 1.)
        a:  透過(0. - 1.)
    Example:
        赤: (H,S,V) = (0,1,0)
        緑: (H,S,V) = (120,1,0)
        青: (H,S,V) = (240,1,0)
    """
    Hi = np.mod(np.floor(H / 60), 60)
    f = H / 60. - Hi
    p = V * (1. - S)
    q = V * (1. - f * S)
    t = V * (1. - (1. - f) * S)

    if Hi == 0:
        rgb = [V, t, p]
    elif Hi == 1:
        rgb = [q, V, p]
    elif Hi == 2:
        rgb = [p, V, t]
    elif Hi == 3:
        rgb = [p, q, V]
    elif Hi == 4:
        rgb = [t, p, V]
    elif Hi == 5:
        rgb = [V, p, q]
    else:
        rgb = [-1, -1, -1]

    if 0:
        print '-------------------'
        print '[H,S,V,A] = ', H, S, V, A
        print '[Hi, f, p, q, t] = ', Hi, f, p, q, t
        print 'rgb = ', rgb

    return rgb
