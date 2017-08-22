# -*- coding: utf-8 -*-
'''
Spyder Editor

This script outputs plots of loaded encoder delta's before and after 
post-processing to no-load calibration data.
'''
import numpy as np
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

plot_num = 0
sig = 2
w = 500
wl_ = 50

cal_case = '90to450_1'
load_ = ''
load_case = '90to450_1'

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/'
f_2_5k = '08032017_/50Hz_0to3240000.csv'
f_200k = '08032017_/5kHz_200ks/5kHz_200ks_0_3520000.csv'
f_155k = '08082017_/calcurve/calcurve_full.csv'

def print_min_max(wave):
    w_min = min(wave[:,1])#/(6.169445)
    p_min = wave[(wave[:,1].argmin()),0]
    w_max = max(wave[:,1])/(6.169445)
    print("Min: ", w_min)
    print("Min_x: ", p_min)
    #print("Max: ", w_max)
    band = w_min-w_max
    print("Band: ", band)

#import unloaded csv
raw_wave = np.genfromtxt(file_prefix + f_2_5k, delimiter = ',', skip_header = True)
#raw_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
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
load_1_2 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_1_2, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)

waves = [filtered_wave, smooth_wave]
labels = ['1.2Nm_filtered', '1.2Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)


#filter and plot rodendplate (3.9Nm) curve
load_3_9 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/rodendplate/rodendplate_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_3_9, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['3.9Nm_filtered', '3.9Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)


#filter and plot 5lbs (9Nm) curve
load_9_0 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/5lbs/5lbs_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_9_0, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['9.0Nm_filtered', '9.0Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)


#filter and plot 7.5lbs (11.5Nm) curve
load_11_5 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/7_5lbs/7_5lbs_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_11_5, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['11.5Nm_filtered', '11.5Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)


#filter and plot 10lbs (14Nm) curve
load_14_0 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/10lbs/10lbs_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_14_0, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['14.0Nm_filtered', '14.0Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)
 
   
#filter and plot 15lbs (19.2Nm) curve
load_19_2 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/15lbs/15lbs_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_19_2, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['19.2Nm_filtered', '19.2Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)


#filter and plot 20lbs (24.2Nm) curve
load_24_2 = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/20lbs/20lbs_125_0Hz_' + load_case + '.csv', delimiter = ',', skip_header = True)
filtered_wave = adjust_load(load_24_2, calibration_wave = cal_wave, sigma = sig)
smooth_wave = moving_avg(filtered_wave, win_len=wl_)
   
waves = [filtered_wave, smooth_wave]
labels = ['24.2Nm_filtered', '24.2Nm_moving_average']
markers = ['bo', 'ro']
scaling = [True, True]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)
#print_min_max(smooth_wave)
