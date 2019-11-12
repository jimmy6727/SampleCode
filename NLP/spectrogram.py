import wave
import struct
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def Rect_Window(soundfile, width, samp_rate, step):
    # soundfile is string of .wav file in local directory
    # Calculate size of soundfile slices we need, in number of frames
    # Width and step size given in milliseconds, sample rate is 44100 in this example.
    # Example calculation: Width = 25 ms, sample rate is 44100:
    # 44100 samples/sec = 44.1 samples / ms 
    # 25 ms = 1102.5 samples (We will use 1102 samples in each of our 25ms windows)
    
    s_per_ms = math.floor(samp_rate/1000)
    ww = s_per_ms*width
    step_in_samples = s_per_ms*step
    
    f = wave.open(soundfile, 'rb')
    l = f.getnframes()
    
    fd = []
    for i in range(l):
        frame = f.readframes(1)
        framedata = struct.unpack('h', frame)
        fd.append(int(framedata[0]))
    
    
    window_data = []
    for i in range(0,l-ww,step_in_samples):
        temp = []
        for j in range(i, i + ww):
            temp.append(fd[j])
        window_data.append(temp)
    
    return window_data
    
def Fourier(window_data, width, samp_rate):
    
    ft_wd = []
    for i in window_data:
        mags = []
        array = np.fft.fft(i)
        for k in array:
           j = np.sqrt((np.square(k.imag)) + (np.square(k.real)))
           logj = 10*math.log10(j)
           mags.append(logj)
        ft_wd.append(mags)

    return(ft_wd)

# Open file and get number of samples
f = sys.argv[1]
file = wave.open(f, 'rb')
l = file.getnframes()

## Get list of windows and length of soundfile for use in plot
a = Rect_Window(f, 25, 44100, 10)
flen_in_windows = len(a)

# Fourier Transform
b = Fourier(a, 25, 44100)

# Transpose data (pcolormesh function requires this format)
# and use only the first half 
c = list(map(list, zip(*b)))
c = c[:(int(math.floor(0.5*len(c))))]


# Function to format y axis (Frequency)
def frequency(x, pos):
    # x is value, pos is tick position
    # We need to scale turn the y values into frequencies according
    # to our window size, which is 25ms.
    # A wave that repeats once within a 25 ms window has frequency
    # 1cycle/25ms * 1000ms/sec = 40 Hz = 0.04 KHz
    return '%1.1f kHz' % (x*.04)

# Function to format x axis (Time)
def time(x, pos):
    global flen_in_windows
    # x is value, pos is tick position
    # We need to scale turn the y values into frequencies according
    # to our window size, which is 25ms.
    # 1sec/44100 samples * 1102 samples/window
    return '%1.1fs' % (x/flen_in_windows)

# Plug into FuncFormatter 
yformatter = FuncFormatter(frequency)
xformatter = FuncFormatter(time)

# Instantiate plot and axes
fig, ax = plt.subplots()

# Set axes and labels
ax.yaxis.set_major_formatter(yformatter)
ax.xaxis.set_major_formatter(xformatter)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (kHz)")

# pcolormesh, add intensity bar
fig = plt.pcolormesh(c, cmap = 'Greys', )
cbar = plt.colorbar(fig, ticks = range(1))
cbar.set_label("Intensity (Highest intensity darkest)", labelpad = 20, rotation = 270)

plt.show()
