'''
This file holds functions used in encoder data
post-processing

'''

import numpy as np
import matplotlib.pyplot as plt

sf = 6.169445
sig = 3
w = 250
fact_ = 1

def calibration_wave(wave, *filepath, width = w, scale_factor = sf, sigma = sig):
    #if filepath is None:
    full_wave_sorted = wave
#    elif wave is None:
#        full_wave_sorted = np.genfromtxt(filepath, delimiter=',', skip_header=True)
#    else:
#        print ('ERROR: No data set given')
#        return
    #full_wave_sorted = np.absolute(full_wave_sorted)
    m = full_wave_sorted[:,0].size
    interval = m/width
    #print (width)
    new_average = np.zeros((width,4))

    #for loop to cycle through the subsets defined by the width
    for i in range(1, width):
    #average the count value for the given array subset width (index 0)
        count_average = np.mean(full_wave_sorted[int((i-1)*interval):int(i*interval),0])
       
    #average the delta value for the given array subset width (index 1)
        delta_average = np.mean(full_wave_sorted[int((i-1)*interval):int(i*interval),1])
        
    #return the std_dev value for the given array subset width
        delta_std = np.std(full_wave_sorted[int((i-1)*interval):int(i*interval),1])
        
    #return the variance value for the given array subset
        delta_var = np.var(full_wave_sorted[int((i-1)*interval):int(i*interval),1])

    #store the average count value in a new array (index 0)
        new_average[i-1,0] = count_average

    #store the average delta value in a new array (index 1)
        new_average[i-1,1] = delta_average
        
    #store the std_dev value in a new array (index 2)
        new_average[i-1,2] = delta_std
        
    #store the var values in a new array (index 3)
        new_average[i-1,3] = delta_var

    return new_average
         
def adjust_load(wave, *filepath, calibration_wave, width = w, sigma = sig):
    #if filepath is None:
    loaded_wave = wave
    c_wave = calibration_wave

    #    elif wave is None:
#        loaded_wave = np.genfromtxt(filepath, delimiter=',', skip_header=True)
#    else:
#        print ('ERROR: No data set given')
#        return
  
    #loaded_wave = np.absolute(loaded_wave)
    c = c_wave[:, 0].size
    p = loaded_wave[:,0].size
    load_adjusted= np.zeros((p,2))

    for i in range(0,p):
        load_adjusted[i,0] = loaded_wave[i,0]
        
        for j in range(0,c):
            if c_wave[j, 0] == loaded_wave[i, 0]:
                load_adjusted[i,1] = loaded_wave[i,1] - c_wave[j,1]
                            
    return load_adjusted

def smooth(x,window_len=100,window='hanning'):
    '''smooth the data using a window with requested size.
    
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
    '''

    #if x.ndim != 1:
        #raise ValueError: 'smooth only accepts 1 dimension arrays.'

    #if x.size < window_len:
        #raise ValueError: 'Input vector needs to be bigger than window size.'


    if window_len<3:
        return x


    #if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
     #   raise ValueError, 'Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman''


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[int(window_len/2-1):-int(window_len/2)]

def plot_wave(wave, title, style, plot_num, use_sf):
    
    n = len(wave)

    plt.figure(plot_num)
    for i in range(0,n):

        if use_sf[i] == 1:
            scale = sf
        else:
            scale = 1

        plt.plot(wave[i][:,0], wave[i][:,1]/scale, style[i])
    plt.legend(title)

def moving_avg(wave, win_len):
    avg_y = smooth(wave[:,1], window_len = win_len)
    avg_curve = np.vstack((wave[:,0], avg_y)).T
    return avg_curve