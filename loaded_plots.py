# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 14:56:58 2017

@author: trandhawa
"""

import numpy as np
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

plot_num = 0

sig = 2

#unloaded wave
unloaded_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [unloaded_wave]
label = ['unloaded']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 1, sf_bool)

rodcollar_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/rodcollar/rodonly_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [rodcollar_wave]
label = ['1.6Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 2, sf_bool)

rodendplate_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/rodendplate/rodendplate_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [rodendplate_wave]
label = ['3.9Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 3, sf_bool)

fivelb_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/5lbs/5lbs_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [fivelb_wave]
label = ['9Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 4, sf_bool)

sevenlb_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/7_5lbs/7_5lbs_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [sevenlb_wave]
label = ['11.5Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 5, sf_bool)

tenlb_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/10lbs/10lbs_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [tenlb_wave]
label = ['14.0Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 6, sf_bool)

fifteenlb_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/15lbs/15lbs_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [fifteenlb_wave]
label = ['19.2Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 7, sf_bool)

twentylb_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/20lbs/20lbs_125_0Hz_90to450_1.csv', delimiter=',', skip_header = True)
wave = [twentylb_wave]
label = ['24.2Nm']
style = ['ro']
sf_bool = [False]
plot_wave(wave, label, style, 8, sf_bool)