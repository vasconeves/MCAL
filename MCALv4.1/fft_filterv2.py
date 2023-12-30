#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from numpy import fft as fft


def fft_filter(y):

    N = len(y)
    step = 0.01
    samp = 20 #it may be necessary to change this setting to fine tune the filter

    # FFT Filtering
    yfft = []
    fourier = []

    for i in xrange(N):
        fourier.append(fft.fft(y[i]))
        n = len(fourier[-1])
        freq = fft.fftfreq(n, d=step)
        iy = np.zeros(n, dtype=complex)

        for j in xrange(n):
            if -samp < freq[j] and freq[j] < samp:
                iy[j] = fourier[-1][j]
            else:
                iy[j] = 0
        yfft.append(np.real(fft.ifft(iy, n)))

    return yfft
