# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 11:05:00 2017

@author: trandhawa
"""

import numpy as np
import csv
from scipy import stats
import matplotlib.pyplot as plt
from calibration_fxns import cal_interp, finish_array, adjust_load, delt_torque, calc_delt, parse_csv

#Define the filepath and names to be analyzed
type_ = '50009900'
pref_ = '00'
sn_ = '13'


file_prefix = 'C:/Users/Owner/My SecuriSync/spyder/Torque_Testbench/'
#file_prefix = 'U:/spyder/Torque_Testbench/'
#file_prefix = 'U:/Torque_Calibration/' + type_ + '_' + pref_ + sn_ + '_BLK2/'
#file_prefix = 'U:/Torque_Calibration/'
#file_n = 'run 0 min.csv'
#torque_n = 'loaded_0_min.csv'


file_n = type_ + '_' + pref_ + sn_ + '_unloaded.csv'

file_ = file_prefix + file_n
#torque_f = file_prefix + torque_n

#Parse the calibration run output
#store Input and Output lists
signals_ = ['Input', 'Output']

data_ = parse_csv(file_n, signals_)