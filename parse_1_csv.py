# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:52:28 2017

@author: trandhawa
"""

import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt
from calibration_fxns import cal_interp, finish_array, adjust_load, delt_torque, calc_delt

#Define the filepath and names to be analyzed
#file_prefix = 'C:/Users/Owner/My SecuriSync/trandhawa (mss01-nasusers)/spyder/Torque_Testbench/'
#file_prefix = 'U:/spyder/Torque_Testbench/'
#file_prefix = 'U:/Torque_Calibration/50009880_0008_BLK2/'
file_prefix = 'U:/Torque_Calibration/'
#file_n = 'run 0 min.csv'
#torque_n = 'loaded_0_min.csv'

run = ['-250', '-500', '-750', '-1000', '-1250', '1250', '1000', '750', '500', '250']

file_n = 'unloaded_50009880_10'
type_ = '_BLK2.csv'
torque_n = 'highload_50009880_10_BLK2.csv'

for i in range (0, len(run)):
    file_ = file_prefix + file_n + run[i] + type_
    
    #Parse the calibration run output
    #store Input and Output lists
    with open(file_) as csvfile:
        reader = csv.DictReader(csvfile)
        data_input = []
        data_output = []
        for row in reader:
            data_input.append(row['Input'])
            data_output.append(row['Output'])
    
    #Convert csv values to int 4890
    data_input = np.asarray(data_input[0:], dtype=np.float32)
    data_output = np.asarray(data_output[0:], dtype=np.float32)
    
    data_input = data_input.astype(np.int)
    data_output = data_output.astype(np.int)
    
    #Calculate and store the post-processed data, calibration
    #data and interpolation function used to generate a
    #calibration curve.
    sorted_, cal_curve, int_fxn, direction_ = calc_delt(data_input, data_output)
    
    #Plot the post-processed nominal error curve
    plt.figure(1)
    plt.plot(sorted_[:,0], sorted_[:,1], 'b1')
    plt.show()
    
    #Plot the calibration curve
#    plt.figure(2)
#    plt.plot(cal_curve[:,0], cal_curve[:,1], 'b1')
#    plt.show()
    
    #Open and write to a .csv file that will store the
    #calibration curve
    with open('calib_123.csv', 'w') as csvfile:
        writer_ = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
        writer_.writerow(['Pos', 'Delta'])
        for i in range(cal_curve[:,0].size):
            pos_ = int(cal_curve[i,0])
            delt_ = float(cal_curve[i,1])
            writer_.writerow([pos_, delt_])
    
    #Use the calibration curve to flatten the nominal error
    #curve and view the error 'band'
    cal_flat = sorted_[:,1] - int_fxn(sorted_[:,0])
   
    #Calculate the amplitude of the nominal error curve
    nominal_amp = np.max(sorted_[:,1]) - np.min(sorted_[:,1])
    
    #Calculate the standard deviation about the nominal error
    #curve
    nominal_std = np.std(cal_flat)
    
    #Calculate the average 'band' width of the nominal error
    nominal_avg = np.average(cal_flat)