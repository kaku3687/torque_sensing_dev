# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:01:17 2017

@author: trandhawa
"""

import numpy as np
import matplotlib.pyplot as plt
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

plot_num = 0
w = 60
sig = 1
date_ = ''
load_amt = '20lbs'
load_case = '90to450_1'

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/'
f_2_5k = '08032017_/50Hz_0to3240000.csv'
f_200k = '08032017_/5kHz_200ks/5kHz_200ks_0_3520000.csv'

def print_min_max(wave):
    w_min = min(wave[:,1])#/(6.169445)
    w_max = max(wave[:,1])/(6.169445)
    print("Min: ", w_min)
    print("Max: ", w_max)
    band = w_min-w_max
    print("Band: ", band)

#import unloaded csv
raw_wave = np.genfromtxt(file_prefix + f_200k, delimiter = ',', skip_header = True)
cal_wave = calibration_wave(raw_wave, width = w, sigma = sig)
#cal_wave = calibration_wave('C:/Users/trandhawa/Desktop/unloaded_125_0Hz_90to450_1.csv')
newx = cal_wave[:,0]
newy = cal_wave[:,1]
newstd = cal_wave[:,2]
cal_spos = np.column_stack((newx, newy+sig*newstd))
cal_sneg = np.column_stack((newx, newy-sig*newstd))

#plot calibration wave from unloaded data
waves = [cal_wave, cal_spos, cal_sneg]
labels = ['Calibration_Wave', 'Calibration+2sig', 'Calibration-2sig']
markers = ['go', 'bo', 'ro']
scaling = [False, False, False]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)


#filter and plot rodonly (1.2Nm) curve
load_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/'+ load_amt +'/'+ load_amt +'_125_0Hz_' + load_case + '_wTorque.csv', delimiter = ',', skip_header=True)
filtered_wave = adjust_load(load_wave, calibration_wave = cal_wave, width = w, sigma = sig)
torque_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/'+ load_amt +'/'+ load_amt +'_125_0Hz_'+ load_case + '_wTorque.csv', delimiter=',', skip_header=True)
torque_wave = torque_wave[:, [0,2]]
torque_wave[:,1] = torque_wave[:,1]*(144.15/2048)
smooth_wave = moving_avg(filtered_wave)

#waves = [filtered_wave, smooth_wave, torque_wave]
#labels = ['23.5Nm_filtered', '23.5Nm_moving_average', 'Torque_Sensor']
#markers = ['bo', 'ro', 'g1']
#scaling = [False, False, False]
#
#plot_num += 1
#
#plot_wave(waves, labels, markers, plot_num, scaling)
#
#waves = [torque_wave]
#labels = [ 'Torque_Sensor']
#markers = ['g1']
#scaling = [False]
#
#plot_num += 1
#
#plot_wave(waves, labels, markers, plot_num, scaling)

fig, f_ax= plt.subplots()
f_ax.plot(filtered_wave[:,0], filtered_wave[:,1]/(6.169445), 'b1')
f_ax.plot(smooth_wave[:,0], smooth_wave[:,1]/(6.169445), 'r.')
f_ax.set_xlabel('Counts')
f_ax.set_ylabel('Delta', color='b')
f_ax.tick_params('y', colors='b')

t_ax = f_ax.twinx()
t_ax.plot(torque_wave[:,0], torque_wave[:,1])
t_ax.set_ylabel('Torque (Nm)', color='g')
t_ax.tick_params('y', colors='g')

c_ax = f_ax.twinx()
c_ax.plot(newx, newy/(6.169445), 'yx')
c_ax.set_ylabel('Calibration Wave', color = 'y')
c_ax.tick_params('y', colors='y')

fig.tight_layout()
plt.show()