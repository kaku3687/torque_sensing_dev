# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:19:44 2017

@author: trandhawa
"""

import numpy as np
from scipy.interpolate import interp1d
import csv


#FUNCTION to remove repeat values from curve for interpolation
def remove_repeat(f_x):
       
    #identify indices with non-repeating values (along x-axis)
    vals, idx = np.unique(f_x[:,0], return_index = True)
   
    f_ = np.zeros((idx.size, 2))
    
    #loop through and populate new array with the indices of the unique 
    #values for both x and y
    for i in range(0, idx.size):
        f_[i,0] = f_x[idx[i], 0]
        f_[i,1] = f_x[idx[i], 1]
    
    #return the cleaned array
    return f_


#FUNCTION to create a moving average of a sample set
def smooth(x,window_len=50,window='hanning'):
    if window_len<3:
        return x

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[int(window_len/2-1):-int(window_len/2)]

#FUNCTION to create a moving across an entire wave/data set
def moving_avg(wave, win_len=500):
    avg_y = smooth(wave[:,1], window_len = win_len)
    avg_curve = np.vstack((wave[:,0], avg_y)).T
    return avg_curve

#FUNCTION to remove outliers from a sample set
def reject_outliers(data, m = 2):
    return data[abs(data-np.mean(data)) < m*np.std(data)]

#FUNCTION to create interpolation function for curve
def cal_interp(cal, rev_cnt_ = 524288):
     
    #remove repeating values from curve
    cal_curve = remove_repeat(cal)
    
    #smooth curve with moving average
    cal_curve = moving_avg(cal_curve)
    
    #generate interpolation function
    f_itp = interp1d(cal_curve[:,0], cal_curve[:,1], kind='cubic')
    
    #create x-array for 1 full rev wrt input encoder values
    fx_ = np.arange(0,rev_cnt_,1)
    
    #generate y-array using x-array and interpolation function
    fy_ = f_itp(fx_)
    
    f_ = np.vstack((fx_, fy_)).T
    
    return f_, f_itp

#FUNCTION to complete array over full rev of output for interpolation function
def finish_array(data_sort, indices_, insert_, p_, in_ = 0):
    missing_o = insert_
    missing_i = []
    for i in range(missing_o.size):
        temp_value = p_[0]*(missing_o[i]**3) + p_[1]*(missing_o[i]**2) + p_[2]*(missing_o[i]**1) + p_[3]*(missing_o[i]**0)
        missing_i.append(temp_value)
    
    if(in_ == 1):
        cal_out = np.insert(data_sort[:,0], indices_, missing_o)
        cal_delta = np.insert(data_sort[:,1], indices_, missing_i)
    else:
        cal_out = np.append(data_sort[:,0], missing_o)
        cal_delta = np.append(data_sort[:,1], missing_i)
        
    cal_ = np.vstack((cal_out, cal_delta)).T
    
    return cal_

#FUNCTION to adjust delta from a loaded wave using a calibration wave
def adjust_load(wave, *filepath, calibration_wave):
    #if filepath is None:
    loaded_wave = wave
    c_wave = calibration_wave

    p = loaded_wave[:,0].size
    load_adjusted= np.zeros((p,2))

    for i in range(0,p):
        load_adjusted[i,0] = loaded_wave[i,0]
        load_adjusted[i,1] = loaded_wave[i,1] - c_wave[int(loaded_wave[i,0]),1]
                                   
    return load_adjusted

#FUNCTION to parse a csv file and n 1-D arrays given a set of headers in
#   a csv file to look for.
def parse_csv(filename, signals):
    num_sigs = len(signals)

    data_ = np.empty()

    for i in range(num_sigs):
        data_[i,] = np.asarray()

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for column in range(num_sigs):
            for row in reader:
                data_[column,:].append(row[signals[column]])

    return data_


##OBS FUNCTION to parse a csv 
##TO-DO: Re-write this function to accept a set of lists corresponding to 
##   data headers that will be extracted from a data set
#def parse_csv(filename):
#    abs_res = 524287
#    rel_res = 20216
#    g_ratio = 160
#
#    with open(filename) as csvfile:
#        reader = csv.DictReader(csvfile)
#        data_input = []
#        data_output = []
#        for row in reader:
#            data_input.append(row['Input'])
#            data_output.append(row['Output'])
#
#    data_input = np.asarray(data_input, dtype=np.float32)
#    data_output = np.asarray(data_output, dtype=np.float32)
#
#    data_input = data_input.astype(np.int)
#    data_output = data_output.astype(np.int)
#
#    dir_ = 1
#
#    if np.sign(data_input[50] - data_input[5]) == np.sign(data_output[50] - data_output[5]):
#        dir_ = 1
#    else:
#        dir_ = -1
#
#    conv_fact_ = abs_res/(rel_res * g_ratio)
#    data_input = data_input*(conv_fact_)*dir_
#
#    out_min = np.min(data_output)
#    data_output = data_output - out_min
#
#    #Calculate Delta
#    data_delta = data_output - data_input
#
#    #Write .csv file with output position vs delta
#    # plt.figure(1)
#    # plt.plot(data_output, data_delta, 'b1')
#    # plt.show()
#
#    cal_wave = np.vstack((data_output, data_delta)).T
#
#    cal_std = cal_interp(cal_wave[:,:], rev_cnt_ = abs_res)
#
#    # plt.figure(2)
#    # plt.plot(cal_std[:,0], cal_std[:,1], 'b1')
#    # plt.show()
#
#    return cal_std, dir_

#FUNCTION to calculate the delta (nominal) from a data set wrt
#   output position
def calc_delt(input_, output_):
    abs_res = 524288
    rel_res = 20216
    g_ratio = 160

    dir_ = 1

    if np.sign(input_[50] - input_[5]) == np.sign(output_[50] - output_[5]):
        dir_ = 1
    else:
        dir_ = -1

    #use multip to convert input to output
    conv_fact_ = abs_res/(rel_res * g_ratio)
    input_ = input_*(conv_fact_)*dir_

    delta_ = output_ - input_

    #out_min = np.min(data_output)
    #data_output = data_output - out_min
    data_mod = np.mod(output_, abs_res)

    data_ = np.vstack((data_mod, delta_)).T
    data_sort = data_[data_[:,0].argsort()]

    #Calculate Delta
    #data_delta = data_sort[:,0] - data_sort[:,1]
    #data_delta = reject_outliers(data_delta)

    #Write .csv file with output position vs delta
    
    #Complete array
    front_ = np.arange(0, np.min(data_sort[:,0]))
    front_i = [0]
    p_ = np.polyfit(data_sort[:100, 0], data_sort[:100, 1], 3)
    temp_ = finish_array(data_sort, front_i, front_, p_, in_ = 1)

    end_ = np.arange(np.max(temp_[:,0]), abs_res)
    end_i = np.arange(temp_[:,0].size, temp_[:,0].size + end_.size)
    size_ = temp_[:,0].size
    p_ = np.polyfit(temp_[(size_-100):size_, 0], temp_[(size_-100):size_, 1], 3)
    cal_wave = finish_array(temp_, end_i, end_, p_)

    cal_std, interp_ = cal_interp(cal_wave[:,:], rev_cnt_ = abs_res)

    return data_sort, cal_std, interp_, dir_

#FUNCTION to calculate the torque given an adjusted delta
def delt_torque(input_, output_, torque_, cal_):
    abs_res = 524288
    rel_res = 20216
    g_ratio = 160
    adc_res = 2048
    rxn_max = 14415 #N-cm

    dir_ = 1

    if np.sign(input_[50] - input_[5]) == np.sign(output_[50] - output_[5]):
        dir_ = 1
    else:
        dir_ = -1

    #use multip to convert input to output
    conv_fact_ = abs_res/(rel_res * g_ratio)
    input_ = input_*(conv_fact_)*dir_

    delta_ = output_ - input_
    data_mod = np.mod(output_, abs_res)
    #out_min = np.min(data_output)
    #data_output = data_output - out_min
    t_val = torque_*(rxn_max/adc_res)
    wave_ = np.vstack((data_mod, delta_)).T

    outvsdelta = adjust_load(wave = wave_, calibration_wave = cal_)
    delta_ = outvsdelta[:,1]

    data_ = np.vstack((delta_, t_val, data_mod)).T

    t_delta = data_[data_[:,0].argsort()]

    return t_delta
