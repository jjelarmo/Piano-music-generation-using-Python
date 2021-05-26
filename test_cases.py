# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:52:41 2021

@author: Jesmar.Elarmo
"""

import Analysis
import Synthesis
import numpy as np
from scipy.io import wavfile

note_freqs = Synthesis.get_piano_notes()
frequency = note_freqs['C4']
frequency_2 = note_freqs['D5']

note_C4 = Analysis.SinSignal(frequency,2048.0,0)
note_C4_wave = note_C4.make_wave(5.0,0, frequency*10)
#note_C4_wave.write_wav_file('C4.wav')
note_C4_spectrum = note_C4_wave.make_spectrum(False)
#note_C4_spectrum.plot()

note_D5 = Analysis.SinSignal(frequency_2,2048.0,0)
note_D5_wave = note_D5.make_wave(5.0,0, frequency_2*2)
note_D5_spectrum = note_D5_wave.make_spectrum(False)
#note_D5_spectrum.plot()

new_note = note_D5 + note_C4
new_note_wave = new_note.make_wave(5.0,0, frequency*10)
new_note_spectrum = new_note_wave.make_spectrum(False)
#new_note_spectrum.plot()

wav_sample_rate, middle_c = wavfile.read('data_piano_c.wav')
middle_c_wave = Analysis.Wave(middle_c, np.arange(middle_c.shape[0]), wav_sample_rate)
#middle_c_wave.plot(2000)
middle_c_spectrum = middle_c_wave.make_spectrum(False)
#middle_c_spectrum.plot(2000)

synth_c = Synthesis.create_note(frequency, 2048, 6)
synth_c_wave = synth_c.make_wave(1.5,0,44100)
weights = Synthesis.get_adsr_weights(frequency, duration=1.5, length=[0.05, 0.25, 0.55, 0.15],
                           decay=[0.1,0.02,0.005,0.1], sustain_level=0.3)

synth_c_wave.ys = synth_c_wave.ys * weights
synth_c_wave.ys = synth_c_wave.ys*(4096/np.max(synth_c_wave.ys))
synth_c_wave.write_wav_file('synth_c_adsr.wav')
synth_c_wave.plot(15000)
synth_c_spectrum = synth_c_wave.make_spectrum(False)
#ynth_c_spectrum.plot(2000)
