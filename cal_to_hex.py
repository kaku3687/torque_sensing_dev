# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 11:05:00 2017

@author: trandhawa
"""

import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt
from calibration_fxns import cal_interp, finish_array, adjust_load, delt_torque, calc_delt, parse_csv, moving_avg

def calc_address():

    return

def conv_data():
    return

def calc_databytes():
    return

def calc_checksum(bb, aa, dd):
    check_ = bb + aa + dd
    check_ = check_ ^ 0xff
    check_ = check_ + 1
    check_ = check_ & 0xff

    return check_

#Define the filepath and names to be analyzed
type_ = '50009900'
sn_ = '7'


#file_prefix = 'C:/Users/Owner/My SecuriSync/Torque_Testbench/'
file_prefix = 'U:/spyder/Torque_Testbench/'
#file_prefix = 'U:/Torque_Calibration/' + type_ + '_' + pref_ + sn_ + '_BLK2/'
#file_prefix = 'U:/Torque_Calibration/'
#file_n = 'run 0 min.csv'
#torque_n = 'loaded_0_min.csv'

file_n = 'unloaded_' + type_ + '_' + sn_ + '_BLK2.csv'
file_t = 'highload_' + type_ + '_' + sn_ + '_BLK2.csv'

file_ = file_prefix + file_n
torque_f = file_prefix +file_t

####UNLOADED DATA####
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


####LOADED DATA####
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
        
#Convert data from strings to int
t_input = np.asarray(t_input, dtype=np.float32)
t_output = np.asarray(t_output, dtype=np.float32)
t_torque = np.asarray(t_torque, dtype=np.float32)

t_input = t_input.astype(np.int)
t_output = t_output.astype(np.int)
t_torque = t_torque.astype(np.int)

#Post-process the loaded run for the raw delta curve
sorted_t, cal_t, intfxn_t, d_ = calc_delt(t_input, t_output)

#Calculate the loaded delta using the calibration curve
#tvsdelta is returned from the delt_torque function as a 
#3 column array with delta, torque and output_pos in columns
#0, 1 and 2, respectively
tvsdelta = delt_torque(t_input, t_output, t_torque, cal_curve)

tvsdelta = moving_avg(tvsdelta)

td_cal = np.vstack((tvsdelta[:,0], tvsdelta[:,1])).T

#t_, t_itp = cal_interp(td_cal, start_ = -511, rev_cnt_ = 512)
t_, t_itp = cal_interp(td_cal, start_ = np.min(tvsdelta[:,0]), rev_cnt_ = np.max(tvsdelta[:,0]))

#Open and write to a .csv file that will store the
#calibration curve
#Open and write to a .csv file that will store the
#calibration curve
with open('pos_delt_cal.csv', 'w') as csvfile:
    writer_ = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
    writer_.writerow(['Pos_Hex', 'Delta_Hex'])
    for i in range(cal_curve[:,0].size):
        pos_ = int(cal_curve[i,0])
        delt_ = int(cal_curve[i,1])
        writer_.writerow(['{0:04X}'.format(pos_), '{0:04X}'.format(delt_)])

with open('delt_torque_cal.csv', 'w') as csvfile:
    writer_ = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
    writer_.writerow(['AdjDelt_Hex', 'Torque_Hex'])
    for i in range(t_[:,0].size):
        adelt_ = int(t_[i,0])
        torq_ = int(t_[i,1])
        writer_.writerow(['{0:04X}'.format(adelt_), '{0:04X}'.format(torq_)])


cal_hex = "test.hex"
cal_file = open(cal_hex, "w")

address_ = [] #Address array
data_ = [] #Data array
bb_ = 0x02 #Number of bytes in line
tt_ = 0x00 #Line entry type -- data
block_ = 0x0000 #Extended address block -- initialized to 0
block_tt = 0x02 #Line entry type -- extended address
addr_offset = 0x0000

for i in range(len(cal_curve[:,0])):
  
    address_.append((int(cal_curve[i,0]) & 0xffff) + addr_offset)
    
    #Check if address is multiple of FFFF block and add extended address line as needed
    if ((cal_curve[i,0])%0xFFFF)==0:
        cc_ = calc_checksum(bb_, 0, block_)
        cal_file.write(':' + '{0:02X}'.format(bb_) + '{0:04X}'.format(0) + '{0:02X}'.format(block_tt) + '{0:X}'.format(block_).zfill(4) + '{0:02X}'.format(cc_) + '\n')
        block_ = block_ + 16**3
    
    #Calculate checksum and write line to hex file
    data_.append(int(cal_curve[i,1]))
    cc_ = calc_checksum(bb_, address_[-1], data_[-1])
       
    cal_file.write(':' + '{0:02X}'.format(bb_) + '{0:04X}'.format(address_[-1]) + '{0:02X}'.format(tt_) + '{0:X}'.format(data_[-1]).zfill(4) + '{0:02X}'.format(cc_) + '\n')


cal_file.write(":00000001FF")
cal_file.close()

#BBAAAATT[DDDD]CC

#BB Number of data bytes on line


#AAAA Address in bytes


#TT Data Type


#DD Data bytes


#CC Checksum
