# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 21:24:01 2021

@author: Jesmar.Elarmo
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.io import wavfile

PI2 = math.pi * 2

def find_index(x, xs):
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n-1)*(x-start)/(end-start))
    return int(i)

class Spectrum(object):
    
    def __init__(self, hs, fs, framerate, full=False):
        self.hs = np.asarray(hs)
        self.fs = np.asarray(fs)
        self.framerate = framerate
        self.full = full
      
    def amps(self):
        return np.absolute(self.hs)
        
    def plot(self, high=None):
        i = None if high is None else find_index(high, self.fs)
        y_axis = self.amps()
        plt.plot(self.fs[:i], y_axis[:i])
        
class Wave(object):
    
    def __init__(self, ys, ts, framerate):
        self.ys = np.asarray(ys)
        self.ts = np.asarray(ts) 
        self.framerate = framerate
    
    def plot(self, i):
        plt.plot(self.ts[:i], self.ys[:i])
        
    def make_spectrum(self, full=False):
        n = len(self.ys)
        d = 1 / self.framerate
        
        if full:
            hs = np.fft.fft(self.ys)
            fs = np.fft.fftfreq(n, d)
        else:
            hs = np.fft.rfft(self.ys)
            fs = np.fft.rfftfreq(n, d)
        
        return Spectrum(hs, fs, self.framerate, full=False)

    def write_wav_file(self,input_filename='sample.wav'):
        wavfile.write(input_filename, rate=self.framerate, data=self.ys.astype(np.int16))
    
class Signals(object):
    def __add__(self, other):
        
        if other==0:
            return self
        return SumSignals(self, other)
    
    __radd__ = __add__
    
class SumSignals(Signals):
    
    def __init__(self, *args):  #
        self.signals = args
    
    def evaluate(self, ts):
        ts = np.asarray(ts)
        return sum(sig.evaluate(ts) for sig in self.signals)
    
    def make_wave(self, duration=1, start=0, framerate=11025):
        n = round(duration * framerate)
        ts = start + np.arange(n) / framerate
        ys = self.evaluate(ts)
        return Wave(ys, ts ,framerate)
    
class Sinusoid(Signals):
    
    def __init__(self, freq=440, amp=1.0, offset=0, func=np.sin):
        
        self.freq = freq
        self.amp = amp
        self.offset = offset
        self.func = func
        
    def period(self):
        return 1.0/self.freq
    
    def evaluate(self,ts):
        ts = np.asarray(ts)
        phases = PI2 * self.freq * ts + self.offset
        ys = self.amp * self.func(phases)
        return ys
    
    def make_wave(self, duration=1, start=0, framerate=11025):
        n = round(duration * framerate)
        ts = start + np.arange(n) / framerate
        ys = self.evaluate(ts)
        return Wave(ys, ts ,framerate)
        
def CosSignal(freq=440, amp=1.0, offset=0):
    return Sinusoid(freq, amp, offset, func=np.cos)

def SinSignal(freq=440, amp=1.0, offset=0):
    return Sinusoid(freq, amp, offset, func=np.sin)