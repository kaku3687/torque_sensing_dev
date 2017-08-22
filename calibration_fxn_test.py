# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 09:08:11 2017

@author: trandhawa
"""

import numpy as np
import matplotlib.pyplot as plt
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

plot_num = 0
sig = 2

cal_case = '90to450_1'
filename_ = '08022017_'
load_case = '10lbs_50_0Hz_-250kto+6450k_75ks_1_wTorque'

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
unloaded_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_' + cal_case + '.csv', delimiter = ',', skip_header=True)
cal_wave = calibration_wave('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_' + cal_case + '.csv')
#cal_wave = calibration_wave('C:/Users/trandhawa/Desktop/unloaded_125_0Hz_90to450_1.csv')
newx = cal_wave[:,0]
newy = cal_wave[:,1]
newstd = cal_wave[:,2]
cal_spos = np.column_stack((newx, newy+sig*newstd))
cal_sneg = np.column_stack((newx, newy-sig*newstd))

#plot calibration wave from unloaded data
waves = [cal_wave, cal_spos, cal_sneg, unloaded_wave]
labels = ['Calibration_Wave', 'Calibration+2sig', 'Calibration-2sig', 'Unloaded_Wave']
markers = ['go', 'bo', 'ro', 'y']
scaling = [False, False, False, False]

plot_num += 1

plot_wave(waves, labels, markers, plot_num, scaling)