# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:17:56 2017

@author: trandhawa
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 12:53:37 2017

@author: trandhawa
"""
import numpy as np
import matplotlib.pyplot as plt
from processing_fxns import calibration_wave, adjust_load, plot_wave, moving_avg

plot_num = 0

sig = 2

def print_min_max(wave):
    w_min = min(wave[:,1])/(6.169445)
    w_max = max(wave[:,1])/(6.169445)
    print("Min: ", w_min)
    print("Max: ", w_max)
    band = w_min-w_max
    print("Band: ", band)
    
#calculate calibration wave from raw input
cal_wave = calibration_wave('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_90to450_1.csv')
newx = cal_wave[:,0]
newy = cal_wave[:,1]
newstd = cal_wave[:,2]
cal_spos = np.column_stack((newx, newy+sig*newstd))
cal_sneg = np.column_stack((newx, newy-sig*newstd))

unloaded_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/unloaded/unloaded_125_0Hz_90to450_1_wtime.csv', delimiter=',', skip_header=True)

#filter the loaded data using the calibration curve
filtered_wave = adjust_load('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/20lbs/20lbs_125_0Hz_450to90_1.csv', cal_wave)

torque_wave = np.genfromtxt('P:/Motiv/1030_Robotics_Development_IRAD/02_Engineering/IRAD Actuator/Single_Axis_Testing/Testing_Data/Weighted_Testing_PosvsStrain/07272017_/20lbs/20lbs_125_0Hz_450to90_1_wtime.csv', delimiter=',', skip_header=True)
#torque_wave = torque_wave[:, [0,2]]
#torque_wave[:,1] = torque_wave[:,1]*(144.15/2048)
#smooth_wave = moving_avg(filtered_wave)

#plot calibration wave of unloaded delta vs time
#plot the loaded data vs time
#plot the torque data vs time
fig, u_wave = plt.subplots()
u_wave.plot(unloaded_wave[:,0], unloaded_wave[:,2], 'b1')
u_wave.set_xlabel('time (s)')
u_wave.set_ylabel('Delta', color='b')
u_wave.tick_params('y', colors='b')

l_wave = u_wave.twinx()
l_wave.plot(torque_wave[:,0], torque_wave[:,2], 'r1')
l_wave.set_ylabel('loaded_delta', color='r')
l_wave.tick_params('y', colors='r')

t_wave = u_wave.twinx()
t_wave.plot(torque_wave[:,0], torque_wave[:,3]*(144.15/2048), 'g1')
t_wave.set_ylabel('Torque (Nm)', color='g')
t_wave.tick_params('y', colors='g')

fig.tight_layout()
fig.show()