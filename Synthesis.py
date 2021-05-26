# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:49:08 2021

@author: Jesmar.Elarmo
"""
import numpy as np
import Analysis

def get_piano_notes():
    
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 440
    keys =np.array( [x+str(y) for y in range(0,9) for x in octave])
    start = np.where(keys=='A0')[0][0]
    end = np.where(keys=='C8')[0][0]
    keys = keys[start:end+1]
    
    note_freq=dict()
    for n in range(len(keys)):
        note_freq[keys[n]]=round(2**((n+1-49)/12)*base_freq)
    return note_freq

def create_note(fundamental_freq, amplitude, n_harmonics):
    new_note = Analysis.SinSignal(fundamental_freq,amplitude,0)
    harmonics_f = fundamental_freq
    harmonics_amp = amplitude
    for i in range(n_harmonics):
        harmonics_f = fundamental_freq*(i+1)
        harmonics_amp = harmonics_amp * 0.6
        new_note = new_note + Analysis.SinSignal(harmonics_f, harmonics_amp, 0)
    return new_note

#def apply_asr(new_note, duration, attack_time, fundamental_freq):
#    #make_wave(self, duration=1, start=0, framerate=11025)
#    framerate = fundamental_freq * 10
#    period = 1/fundamental_freq
#    
#    if duration % period != 0: #check if my duration is a multiple of my period
#        duration = period*round( duration / period )
#    if attack_time % period !=0:
#        attack_time = period*round( attack_time / period )
#    
#    attack_n = int(attack_time/period)
#    duration_n = int(duration/period)
#    new_note_wave = new_note.make_wave(duration, 0, framerate)
#    amplitude = max(new_note_wave.ys)
#    for n in range(attack_n*10):
#        new_note_wave.ys[n]=(amplitude / attack_time) * new_note_wave.ts[n] * new_note_wave.ys[n]
#    return new_note_wave

def get_adsr_weights(frequency, duration, length, decay, sustain_level, sample_rate=44100):
    '''
    ADSR(attack, decay, sustain, and release) envelop generator with exponential
    weights applied.
    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    duration : float
        Time in seconds.
    length : list
        List of fractions that indicates length of each stage in ADSR.
    decay : list
        List of float for decay factor to be used in each stage for exponential
        weights. 
    sustain_level : float
        Amplitude of `S` stage as a fraction of max amplitude.
    sample_rate : int, optional
        Wav file sample rate. The default is 44100.
    Returns
    -------
    weights : ndarray
    '''
    assert abs(sum(length)-1) < 1e-8
    assert len(length) ==len(decay) == 4
    
    intervals = int(duration*frequency)
    len_A = np.maximum(int(intervals*length[0]),1)
    len_D = np.maximum(int(intervals*length[1]),1)
    len_S = np.maximum(int(intervals*length[2]),1)
    len_R = np.maximum(int(intervals*length[3]),1)
    
    decay_A = decay[0]
    decay_D = decay[1]
    decay_S = decay[2]
    decay_R = decay[3]
    
    A = 1/np.array([(1-decay_A)**n for n in range(len_A)])
    A = A/np.nanmax(A)
    D = np.array([(1-decay_D)**n for n in range(len_D)])
    D = D*(1-sustain_level)+sustain_level
    S = np.array([(1-decay_S)**n for n in range(len_S)])
    S = S*sustain_level
    R = np.array([(1-decay_R)**n for n in range(len_R)])
    R = R*S[-1]
    
    weights = np.concatenate((A,D,S,R))
    smoothing = np.array([0.1*(1-0.1)**n for n in range(5)])
    smoothing = smoothing/np.nansum(smoothing)
    weights = np.convolve(weights, smoothing, mode='same')
    
    weights = np.repeat(weights, int(sample_rate*duration/intervals))
    tail = int(sample_rate*duration-weights.shape[0])
    if tail > 0:
        weights = np.concatenate((weights, weights[-1]-weights[-1]/tail*np.arange(tail)))
    return weights
