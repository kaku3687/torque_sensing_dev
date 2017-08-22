# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:02:27 2017

@author: trandhawa
"""

from scipy import stats, signal
import numpy as np
import matplotlib.pyplot as plt
from processing_fxns import adjust_load, calibration_wave, plot_wave, moving_avg


plot_num = 1
sig_ = 2
w_ = 100
wl_ = 250
win_ = 25
lim_ = 0.1

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/'
date_ = '08212017_/'
testparam_ = '_125Hz_90to450.csv'
load_ = ['noload', 'rodonly', 'rodcollar', '5lb', '10lb', '15lb', '20lb']
momentlow_ = [0, -18, -26, -133, -205, -274, -339]
momenthigh_ = [0, 21, 30, 135, 206, 276, 340]
c_10k = '08042017_/10ks/10ks_25Hz_90to450.csv'
c_2_5k = '08032017_/50Hz_0to3240000.csv'
c_155k = '08082017_/calcurve/calcurve_full.csv'

def print_min_max(wave):
    w_min = min(wave[:2500,1])#/(6.169445)
    w_max = max(wave[:2500,1])#/(6.169445)
    p_min = wave[(wave[:,1].argmin()),0]
    p_max = wave[(wave[:,1].argmax()),0]
#    print("Min: ", w_min, "at: ", p_min)
#    print("Max: ", w_max, "at: ", p_max)
    print("Band: ", (w_max - w_min)/(6.169445*2))
    
cal_wave = np.genfromtxt(file_prefix + date_ + load_[0] + testparam_, delimiter = ',', skip_header = True)
#cal_wave = np.genfromtxt(file_prefix + c_10k, delimiter = ',', skip_header = True)
cal_std = calibration_wave(cal_wave, width = w_)

plt.figure(1)
plt.plot(cal_std[:,0], cal_std[:,1], 'b1')
plt.show()

for i in range (0, len(momenthigh_)):
	plot_num += 1
	moment_ = (momenthigh_[i]/2048)*144.15
	wave_ = np.genfromtxt(file_prefix + date_ + load_[i] + testparam_, delimiter = ',', skip_header = True)
	l_ = adjust_load(wave_, calibration_wave = cal_std)
	avg_ = moving_avg(l_, win_len = wl_)

	print(str(moment_) + 'Nm')
	print_min_max(avg_)
	print('')
	plt.figure(plot_num)
	plt.plot(l_[:,0], l_[:,1], 'r1')
	plt.plot(avg_[:,0], avg_[:,1], 'b1')
	plt.show()

#Increment through loaded wave
#for i in range(0, r):
#    print (i)
#    sum_ = 0
#    num = 0
#    avg_ = 0
#    #Look at values +/- some step size (pos values) around the pos value
#    #we are currently at.
#    for j in range(0, c):
#        #print (j)
#        if cal_wave[j,0] <= (raw_wave[i,0] + low_):
#            j += int((raw_wave[i,0]/cal_wave[j,0]))
#        elif (raw_wave[i,0] + low_) <= cal_wave[j,0] <= (raw_wave[i,0] + high_):
#            sum_ +=cal_wave[j,1]
#            num += 1
#        elif cal_wave[j,0] >= (raw_wave[i,0] + high_):
#            break
#    avg_ = sum_/num
#    new_wave[i,0] = raw_wave[i,0]
#    new_wave[i,1] = raw_wave[i,1] - avg_
#    
#plt.plot(new_wave[:,0], new_wave[:,1], 'b1')
    #Take the average of the delta values and substract? this average from
    #the current delta value in the loaded curve.
    
    #Load this new values and pos value from the loaded curve into a new
    #array.

#raw_wave = signal.resample(raw_wave, 2000)