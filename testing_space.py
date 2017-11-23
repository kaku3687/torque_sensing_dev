# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:02:27 2017

@author: trandhawa
"""

from scipy import stats, signal
import numpy as np
import matplotlib.pyplot as plt
from calibration_fxns import cal_interp, moving_avg, adjust_load


plot_num = 1
wl_ = 35
lim_ = 0.1

file_prefix = 'P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/'
date_ = '09112017_/'
testparam_ = '_125Hz_90to450'

#0911 Test Run
#ftype_ = ['.csv', '.csv']
#suffix_ = ['','']
#load_ = ['noload', 'noload']
#momentlow_ = [0, 0]
#momenthigh_ = [0, 0]

#0831 Test Run
ftype_ = ['.csv', '.csv','.csv','.csv','.csv','.csv','.csv','.csv', '.csv', '.csv', '.csv', '.csv', '.csv']
suffix_ = ['', '_hyst','','','','','','', '', '', '', '', '']
load_ = ['noload', 'noload', 'rodonly', 'rodcollar', 'rodendplate', 'rod2ft', 'rod2ftendplate', '2_5lb', '5lb', '12_5lb', '15lb', '22_5lb', '30lb']
momentlow_ =  [0, 0, -14, -19, -54, -117, -203, -306, -335, -543, -624, -838, -1108]
momenthigh_ = [0, 0,  25,  31,  65,  131,  198,  312,  330,  552,  632,  845,  1113]

#0821 Test Run
#ftype_ = ['.csv','.csv','.csv','.csv', '.csv']
#suffix_ = ['', '', '', '', '']
#load_ = ['noload', 'rodonly', 'rodcollar', '5lb', '10lb']
#momentlow_ =  [0, -18, -26, -133, -205]
#momenthigh_ = [0,  21,  30,  135,  206]

c_10k = '08042017_/10ks/10ks_25Hz_90to450.csv'
c_2_5k = '08032017_/50Hz_0to3240000.csv'
c_155k = '08082017_/calcurve/calcurve_full.csv'


def print_min_max(wave):
    w_min = min(wave[:,1])#/(6.169445)
    w_max = max(wave[:,1])#/(6.169445)
#    p_min = wave[(wave[:,1].argmin()),0]
#    p_max = wave[(wave[:,1].argmax()),0]
#    print("Min: ", w_min, "at: ", p_min)
#    print("Max: ", w_max, "at: ", p_max)
    print("Band: ", (w_max - w_min)/(6.169445))

    
def read_torque(delta, pos, cal_curve):
    
    #look up the offset on the calibration table given the current position
    #this should be implemented so that position can be a range of values
    offset_ = np.zeros((pos.size,2))
    for i in range(0, pos.size):
        offset_[i] = cal_curve[int(pos[i]), 1]
    
    #tare the delta value with respect to the calibration offset
    del_ = np.zeros((delta.size,2))
    for i in range(0, delta.size):
        del_[i] = delta[i] - offset_[i]
    
    #look up the torque value for the given tared delta (how?)
    torque_ = 1.4425*(np.average(del_)/6.169445) + 0.0649   
    pos_ = np.median(pos)
    
    return torque_, pos_

    
cal_wave = np.genfromtxt(file_prefix + date_ + load_[0] + testparam_ + suffix_[0] + ftype_[0], delimiter = ',', skip_header = True)
#cal_wave = np.genfromtxt(file_prefix + c_2_5k, delimiter = ',', skip_header = True)
cal_std = cal_interp(cal_wave[:,:], rev_cnt_ = 3234560)

plt.figure(1)
plt.plot(cal_std[:,0], cal_std[:,1], 'b1')
plt.show()

step_s = 50

for i in range (0, len(momenthigh_)):
    plot_num += 1
    moment_ = (momenthigh_[i]/2048)*144.15
    wave_ = np.genfromtxt(file_prefix + date_ + load_[i] + testparam_ + suffix_[i] + ftype_[i], delimiter = ',', skip_header = True)   
    w_avg_ = moving_avg(wave_[40:,:], win_len=wl_)
    l_ = adjust_load(wave_[40:,:], calibration_wave = cal_std)
    avg_ = moving_avg(l_, win_len = wl_)

    p = w_avg_[:,0].size
    torque_ = np.zeros(int(p/step_s))
    position_ = np.zeros(int(p/step_s))
    
    for k in range(step_s, p-step_s, step_s):
        d_ = w_avg_[(k):(k+step_s), 1]
        p_ = w_avg_[(k):(k+step_s), 0]
        torque_[int((k)/step_s)], position_[int((k)/step_s)] = read_torque(delta=d_, pos=p_, cal_curve=cal_std)

    print(str(moment_) + 'Nm')
    print_min_max(avg_)
    print('')
    
    fig, f_ax = plt.subplots()
#    f_ax.plot(l_[:,0], l_[:,1], 'r1')
    f_ax.plot(avg_[:,0], avg_[:,1], 'b1')
    f_ax.set_xlabel('Position')
    f_ax.set_ylabel('Delta', color = 'b')
    f_ax.tick_params('y', colors='b')
    
    t_ax = f_ax.twinx()
    t_ax.plot(position_, torque_, 'r2')
    t_ax.set_ylabel('Torque (Nm)', color='r')
    t_ax.tick_params('y', colors='r')
    
    fig.tight_layout()    
    plt.show()

