# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:24:46 2017

@author: trandhawa
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 08:33:54 2017

@author: trandhawa
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as sts

#Import csv data files
#CSV on data with unloaded testbed
unloaded_full = np.genfromtxt('C:/Users/trandhawa/Desktop/nofrontend_50_0Hz_2revs.csv', delimiter=',', skip_header=True)
unloadedx = unloaded_full[0:1500,0]
unloadedy = unloaded_full[0:1500,1]

#Create best fit (n=5) polynomial for unloaded case
enc_sine_coeff = np.polyfit(unloadedx, unloadedy, 12)

#Remove best fit values from unloaded and loaded data
#enc_sine_loaded = np.polyval(enc_sine_coeff, loadedx)
unloaded_filter = unloadedy - np.polyval(enc_sine_coeff, unloadedx)

#List avg, std_dev, etc. on new data sets

#Plots
plt.figure(1)
labels=["unloaded", "unloaded_filter"]
plt.plot(unloadedx, unloadedy)
plt.plot(unloadedx, unloaded_filter)
plt.legend(labels)
