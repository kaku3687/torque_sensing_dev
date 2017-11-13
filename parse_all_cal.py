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
type_ = ['50009880', '50009900', '50010350']
sn_ = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
num_type = [10, 15, 2]
#file_p = 'U:/Torque_Calibration/'
file_p = 'P:/Rutgers/1056_Rutgers_Robosimian/02_Engineering/Rutger Actuator Checkout/Torque_Calibration/'


l_type_ = len(type_)
l_num_ = len(num_type)

for i_type_ in range(l_type_):
   
    for j_sn_ in range(num_type[i_type_]):
                
        if j_sn_ <= 8:
            pref_ = '000'
        else:
            pref_ = '00'
        
        file_prefix = file_p + type_[i_type_] + '_' + pref_ + sn_[j_sn_] + '_BLK2/'
        
        file_n = 'unloaded_' + type_[i_type_] + '_' + sn_[j_sn_] + '_BLK2.csv'
        torque_n = 'highload_' + type_[i_type_] + '_' + sn_[j_sn_] + '_BLK2.csv'
        
        file_ = file_prefix + file_n
        torque_f = file_prefix + torque_n
        
        plot_title = type_[i_type_] + '_' + pref_ + sn_[j_sn_] + '_BLK2'
        
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
        plt.title(plot_title)
        plt.plot(sorted_[:,0], sorted_[:,1], 'b1')
        plt.show()
        
        #Plot the calibration curve
        plt.figure(2)
        plt.title(plot_title)
        plt.plot(cal_curve[:,0], cal_curve[:,1], 'b1')
        plt.show()
        
        
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
        
        #Import loaded run data
        with open(torque_f) as csvfile:
            reader = csv.DictReader(csvfile)
            t_input = []
            t_output = []
            t_torque = []
            t_current = []
            for row in reader:
                t_input.append(row['Input'])
                t_output.append(row['Output'])
                t_torque.append(row['Torque'])
                t_current.append(row['Current'])
        
        #Convert data from strings to int
        t_input = np.asarray(t_input, dtype=np.float32)
        t_output = np.asarray(t_output, dtype=np.float32)
        t_torque = np.asarray(t_torque, dtype=np.float32)
        t_current = np.asarray(t_current, dtype=np.float32)
        
        t_input = t_input.astype(np.int)
        t_output = t_output.astype(np.int)
        t_torque = t_torque.astype(np.int)
        t_current = t_current.astype(np.int)
        
        #Post-process the loaded run for the raw delta curve
        sorted_t, cal_t, intfxn_t, d_ = calc_delt(t_input, t_output)
        
        #Calculate the loaded delta using the calibration curve
        #tvsdelta is returned from the delt_torque function as a 
        #3 column array with delta, torque and output_pos in columns
        #0, 1 and 2, respectively
        tvsdelta = delt_torque(t_input, t_output, t_torque, cal_curve)
        
        #Calculate the average output counts/Nm
        cntvst, _intc, _r_v, _p_v, _stdrr = stats.linregress(tvsdelta[:,0], tvsdelta[:,1])
        
        #Flatten the loaded wave
        flat_t = adjust_load(wave = sorted_t, calibration_wave = cal_curve)
        
        fig, f_ax = plt.subplots()
        #    f_ax.plot(l_[:,0], l_[:,1], 'r1')
        f_ax.plot(tvsdelta[:,1], tvsdelta[:,0], 'b1')
        f_ax.set_xlabel('Torque')
        f_ax.set_ylabel('Delta', color = 'b')
        f_ax.tick_params('y', colors='b')
        
        fig.tight_layout()    
        plt.title(plot_title)
        plt.show()