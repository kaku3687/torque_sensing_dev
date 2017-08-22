# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:03:42 2017

@author: trandhawa
"""

import numpy as np
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

def print_min_max(wave):
    w_min = min(wave[:,1])/(6.169445)
    p_min = wave[(wave[:,1].argmin()),0]
    w_max = max(wave[:,1])/(6.169445)
    print("Min: ", w_min)
    print("Min_x: ", p_min)
    print("Max: ", w_max)
    band = w_min-w_max
    print("Band: ", band)

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain'

f_cal_100 = file_prefix + '/08022017_/varying_speed/calibration_125_0Hz_90to450_100ks_1.csv'
f_cal_45 = file_prefix + '/08022017_/varying_speed/calibration_50_0Hz_90to450_45ks_1.csv'
f_cal_30 = file_prefix + '/08022017_/varying_speed/calibration_50_0Hz_90to450_30ks_1.csv'

f_load_100 = file_prefix + '/08022017_/varying_speed/10lbs_125_0Hz_90to450_100ks_1.csv'
f_load_45 = file_prefix + '/08022017_/varying_speed/10lbs_50_0Hz_90to450_45ks_1.csv'
f_load_30 = file_prefix + '/08022017_/varying_speed/10lbs_50_0Hz_90to450_30ks_1.csv'

plot_num = 0

#Load the 3 calibration runs (30, 45 and 100ks)
run_30 = np.genfromtxt(fname = file_prefix + '/08022017_/varying_speed/calibration_50_0Hz_90to450_30ks_1.csv', delimiter = ',', skip_header=True)
run_45 = np.genfromtxt(fname = file_prefix + '/08022017_/varying_speed/calibration_50_0Hz_90to450_45ks_1.csv', delimiter = ',', skip_header=True)
run_100 = np.genfromtxt(fname = file_prefix + '/08022017_/varying_speed/calibration_125_0Hz_90to450_100ks_1.csv', delimiter = ',', skip_header=True)

#Turn them into uniform arrays using the calibration function
calib_30 = calibration_wave(f_cal_30)
calib_45 = calibration_wave(f_cal_45)
calib_100 = calibration_wave(f_cal_100)

#Return the correlation coefficient for each set
corr_30_30 = np.corrcoef(calib_30[:,1], calib_30[:,1])
corr_30_45 = np.corrcoef(calib_30[:,1], calib_45[:,1])
corr_30_100 = np.corrcoef(calib_30[:,1], calib_100[:,1])
corr_45_45 = np.corrcoef(calib_45[:,1], calib_45[:, 1])
corr_45_100 = np.corrcoef(calib_45[:,1], calib_100[:,1])
corr_100_100 = np.corrcoef(calib_100[:,1], calib_100[:,1])


print('30_30', corr_30_30)
print('30_45', corr_30_45)
print('30_100', corr_30_100)
print('45_45', corr_45_45)
print('45_100', corr_45_100)
print('100_100', corr_100_100)

#Use new calibration curve to generate a filtered curve
new_30 = adjust_load(f_load_30, calib_100)
new_45 = adjust_load(f_load_45, calib_100)
new_100 = adjust_load(f_load_100, calib_100)

#Get moving average
smooth_30 = moving_avg(new_30)
smooth_45 = moving_avg(new_45)
smooth_100 = moving_avg(new_100)

#Plot curves
#30ks curves
waves = [new_30, smooth_30]
labels = ['30ks_adjusted', '30ks_moving_average']
markers = ['b1', 'r1']
scale = [True, True]
plot_num += 1
plot_wave(waves, labels, markers, plot_num, scale)

print_min_max(smooth_30)

#45ks curves
waves = [new_45, smooth_45]
labels = ['45ks_adjusted', '45ks_moving_average']
markers = ['b1', 'r1']
scale = [True, True]
plot_num += 1
plot_wave(waves, labels, markers, plot_num, scale)

print_min_max(smooth_45)

#100ks curves
waves = [new_100, smooth_100]
labels = ['100ks_adjusted', '100ks_moving_average']
markers = ['b1', 'r1']
scale = [True, True]
plot_num += 1
plot_wave(waves, labels, markers, plot_num, scale)

print_min_max(smooth_100)