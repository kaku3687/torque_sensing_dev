# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 12:23:50 2017

@author: trandhawa
"""

import numpy as np
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

w_ = 100

def print_min_max(wave):
    w_min = min(wave[:,1])#/(6.169445)
    w_max = max(wave[:,1])#/(6.169445)
    p_min = wave[(wave[:,1].argmin()),0]
    p_max = wave[(wave[:,1].argmax()),0]
    print("Min: ", w_min, "at: ", p_min)
    print("Max: ", w_max, "at: ", p_max)
    

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/'
f_2_5k = '08032017_/50Hz_0to3240000.csv'
f_200k = '08032017_/5kHz_200ks/5kHz_200ks_0_3520000.csv'
plot_num = 0

wave_2_5k = np.genfromtxt(file_prefix + f_2_5k, delimiter = ',', skip_header=True)
wave = [wave_2_5k]
label =  ['2_5k_wave']
marker = ['b1']
scale = [False]

plot_num += 1
#plot_wave(wave, label, marker, plot_num, scale)
print_min_max(wave_2_5k)

cal_2_5k = calibration_wave(file_prefix + f_2_5k, width = w_)
wave = [cal_2_5k]
label =  ['cal_2_5k']
marker = ['b1']
scale = [False]

plot_num += 1
plot_wave(wave, label, marker, plot_num, scale)
print_min_max(cal_2_5k)

wave_200k = np.genfromtxt(file_prefix + f_200k, delimiter = ',', skip_header=True)
wave = [wave_200k]
label =  ['200k_wave']
marker = ['b1']
scale = [False]

plot_num += 1
#plot_wave(wave, label, marker, plot_num, scale)
print_min_max(wave_200k)

cal_200k = calibration_wave(file_prefix + f_200k, width = w_)
wave = [cal_200k]
label =  ['cal_200k']
marker = ['b1']
scale = [False]

plot_num += 1
#plot_wave(wave, label, marker, plot_num, scale)
print_min_max(cal_200k)
