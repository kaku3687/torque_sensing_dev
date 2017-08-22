# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:02:27 2017

@author: trandhawa
"""

import numpy as np
import matplotlib.pyplot as plt
from processing_fxns import adjust_load, calibration_wave, plot_wave, moving_avg

#simulated wave variables
t_num = 3000000
t_step = 300
sim_phase = .1
sim_amp = 2000
sim_offset = 1000
band_high = 100
band_low = -100

pos_num = 3000000
pos_step = 900
delta_amp = 200
delta_high = 10
delta_low = -10
load_phase = 2

#plot variables
w_ = 1500
sig_ = 2.5
wl_ = 250

#initialize position (t) and delta (sim_sin) arrays
t = np.arange(0, t_num, t_step, dtype = int)
sim_sin = np.zeros(np.size(t))

#populate delta wave with sine and random noise
for i in range(0, np.size(t)):
    sim_sin[i] = sim_amp*np.sin((np.pi/sim_phase) + (2*np.pi/t_num)*t[i]) - sim_offset + np.random.randint(band_low, band_high)

#plot raw wave
plt.figure(1)    
plt.plot(t, sim_sin, 'b1')

#build 2-D array for raw wave
raw_wave = np.column_stack((t, sim_sin))

#generate calibration wave
cal_wave = calibration_wave(wave = raw_wave, width = w_, sigma = sig_)

#generate filtered wave from calibration wave
#this filtered wave is a control case. the calibration routine is used
#on the original wave so the output should be (close to) 0.
new_wave = adjust_load(wave = raw_wave, calibration_wave = cal_wave, width = w_, sigma = sig_)

plt.figure(2)
plt.plot(cal_wave[:,0], cal_wave[:,1], 'b1')
plt.plot(new_wave[:,0], new_wave[:,1], 'r1')

#initialize position (pos) and delta (load_sin) arrays
pos = np.arange(0, pos_num, pos_step, dtype = int)
load_sin = np.zeros(np.size(pos))

#populate loaded delta wave with sine and random noise + 'load' data
for i in range(0, np.size(pos)):
    load_sin[i] = (sim_amp*np.sin((np.pi/(sim_phase-.201)) + (2*np.pi/pos_num)*pos[i]) - sim_offset + np.random.randint(band_low, band_high) +
                  delta_amp*np.sin((np.pi/load_phase) + (2*np.pi/pos_num)*pos[i]) + np.random.randint(delta_low, delta_high))

torque_wave = np.zeros(np.size(pos))

for i in range(0, np.size(pos)):
    torque_wave[i] = delta_amp*np.sin((np.pi/load_phase) + (2*np.pi/pos_num)*pos[i]) + np.random.randint(delta_low, delta_high)

torque_wave = np.column_stack((pos, torque_wave))

#plot raw loaded wave
plt.figure(3)
plt.plot(pos, load_sin, 'b1')

#build 2-D array for loaded wave
load_wave = np.column_stack((pos, load_sin))

#generate filtered wave from calibration wave
filtered_wave = adjust_load(wave = load_wave, calibration_wave = cal_wave, width = w_, sigma = sig_)

#generate moving average from filtered wave
smooth_wave = moving_avg(filtered_wave, win_len=wl_)

plt.figure(4)
plt.plot(torque_wave[:,0], torque_wave[:,1], 'r1')

plt.figure(5)
plt.plot(filtered_wave[:, 0], filtered_wave[:, 1], 'r1')
plt.plot(torque_wave[:, 0], torque_wave[:, 1], 'y1')
plt.plot(smooth_wave[:, 0], smooth_wave[:, 1], 'g1')