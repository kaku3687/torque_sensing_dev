# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt

def smooth(x,window_len=100,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    #if x.ndim != 1:
        #raise ValueError: "smooth only accepts 1 dimension arrays."

    #if x.size < window_len:
        #raise ValueError: "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    #if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
     #   raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[int(window_len/2-1):-int(window_len/2)]

#interval size (width)
w = 1250
scale_factor = 6.169445
sig = 2

#import unloaded csv
full_wave_sorted = np.genfromtxt('C:/Users/trandhawa/Desktop/unloaded_125_0Hz_90to450_1.csv', delimiter=',', skip_header=True)
m = full_wave_sorted.size
width = m/w
new_average = np.zeros((w,3))

#for loop to cycle through the subsets defined by the width
for i in range(1, w):
#average the count value for the given array subset width (index 0)
    count_average = np.mean(full_wave_sorted[int((i-1)*width):int(i*width),0])
   
#average the delta value for the given array subset width (index 1)
    delta_average = np.mean(full_wave_sorted[int((i-1)*width):int(i*width),1])
    
#return the std_dev value for the given array subset width
    delta_std = np.std(full_wave_sorted[int((i-1)*width):int(i*width),1])

#store the average count value in a new array (index 0)
    new_average[i-1,0] = count_average

#store the average delta value in a new array (index 1)
    new_average[i-1,1] = delta_average
    
#store the std_dev value in a new array (index 2)
    new_average[i-1,2] = delta_std
    
newx = new_average[:,0]
newy = new_average[:,1]
newstd = new_average[:,2]

plt.figure(1)
labels=["Averaged Data"]
plt.plot(newx, newy/scale_factor, 'bp')    
plt.plot(newx, (newy-sig*newstd)/scale_factor, 'rp')
plt.plot(newx, (newy+sig*newstd)/scale_factor, 'gp')

loaded_wave = np.genfromtxt('C:/Users/trandhawa/Desktop/rodendplate_125_0Hz_90to450_1.csv', delimiter=',', skip_header=True)
p = loaded_wave[:,0].size
load_adjusted= np.zeros((p,2))

plt.figure(2)
plt.plot(full_wave_sorted[:,0], full_wave_sorted[:,1])
plt.plot(loaded_wave[:,0], loaded_wave[:,1], 'ro')
#print("Load_Adjusted array size", load_adjusted.size)
#print("Loaded_Wave array size", p)

for i in range(1, p):
    #print(i)
    for j in range(1, w):
        #print(j)
        if new_average[j-1,0] <= loaded_wave[i-1,0] <= new_average[j,0]:
            if loaded_wave[i-1,1] >= new_average[j-1,1]:
                diff = new_average[j-1,1] + sig*new_average[j-1,2]
            else:
                diff = new_average[j-1, 1] - sig*new_average[j-1,2]
            load_adjusted[i-1,1] = loaded_wave[i-1,1] - diff
            load_adjusted[i-1,0] = loaded_wave[i-1,0]
            #print(load_adjusted[i-1,1])
            break

smooth_wave = smooth(load_adjusted[:,1]/scale_factor)
   
plt.figure(3)
plt.plot(load_adjusted[:,0], load_adjusted[:,1]/scale_factor, 'bo')
plt.plot(load_adjusted[:,0], smooth_wave, 'ro')
#plt.plot(loaded_wave[:,0], loaded_wave[:,1], 'r')        