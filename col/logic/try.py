import time
import os
import ctypes
import numpy as np
import scipy
import scipy.signal as sg
import numpy as np
import matplotlib.pyplot as plt


myFolder = os.path.split(os.path.realpath(__file__))[0]
ddl_path = os.path.join(myFolder, 'cal.so')


cal = ctypes.cdll.LoadLibrary(ddl_path)


data = [1742, 281, 192, 30, 183, 872, 1921, 932, 291, 191,
        291, 1314, 1243, 1721, 1314, 1232, 121, 200, 12, 81,
        1742, 281, 192, 30, 183, 872, 1921, 932, 291, 191,
        291, 1314, 1243, 1721, 1314, 1232, 121, 200, 12, 81,
        1742, 281, 192, 30, 183, 872, 1921, 932, 291, 191,
        291, 1314, 1243, 1721, 1314, 1232, 121, 200, 12, 81
        ]
data = np.array(data)
b, a = sg.butter(7, [0.04, 0.9], 'bandpass')
print(a, b)

result1 = sg.filtfilt(b, a, data)

cache_char = []
for i in range(len(data)):
    if data[i] > 0:
        data_temp = data[i]
    else:
        data_temp = data[i] + 4095
    judge = 0
    cache_char.append(85)
    cache_char.append(170)
    temp = data_temp >> 4
    cache_char.append(temp)
    judge += temp
    temp = (data_temp - temp*16)*16
    temp += data_temp >> 8
    cache_char.append(temp)
    judge += temp
    temp = data_temp % 256
    cache_char.append(temp)
    judge += temp
    cache_char.append(judge % 256)

INPUT_double = ctypes.c_double*30
INPUT_char = ctypes.c_char*360

bandpass_recon = cal.filterCreateBandpass
comb_recon = cal.filterCreateComb
notch_recon = cal.filterCreateNotch
channel_recon = cal.channelNumChange

filt = cal.splitPack2Filter
filt.restype = ctypes.c_int

recv_res = cal.resultReturn
recv_res.restype = ctypes.POINTER(ctypes.c_double)

filter_a = INPUT_double()
filter_b = INPUT_double()

for i in range(len(a)):
    filter_a[i] = a[i]
    filter_b[i] = b[i]

channel_recon(2)
comb_recon(INPUT_double(), INPUT_double(), 0)
notch_recon(INPUT_double(), INPUT_double(), 0)
bandpass_recon(filter_a, filter_b, len(a))

cache_data = b''
for i in range(360):
    cache_data += bytes([cache_char[i]])

data = filt(cache_data, 360)

cache = []

for i in range(data):
    num = 1
    temp = [0]*num
    res = recv_res(i)
    for i in range(num):
        temp[i] = res[i]
    cache.append(temp)
print(cache)
print(result1)













