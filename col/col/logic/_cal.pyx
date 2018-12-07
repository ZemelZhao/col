from __future__ import absolute_import
import platform
import os
import sys
import multiprocessing as mp
import ctypes
import numpy as np
from ctypes import *
import scipy.signal as sg
import configparser
import time

class Cal(mp.Process):
    def __init__(self):
        super(Cal, self).__init__()
        myFolder = os.path.join(os.pardir, 'logic')
        if platform.system() == 'Windows':
            ddl_path = os.path.join(myFolder, 'cal.ddl')
        elif platform.system() == 'Linux':
            ddl_path = os.path.join(myFolder, 'cal.so')
        else:
            ddl_path = os.path.join(myFolder, 'cal.dylib')

        self.INPUT = ctypes.c_char*1500
        self.data2c = b''

        self.cal_file = ctypes.cdll.LoadLibrary(ddl_path)

        self.filt_recon_bandpass = self.cal_file.filterCreateBandpass
        self.filt_recon_bandpass.restype = ctypes.c_int

        self.filt_recon_comb = self.cal_file.filterCreateComb
        self.filt_recon_comb.restype = ctypes.c_int

        self.filt_recon_notch = self.cal_file.filterCreateNotch
        self.filt_recon_notch.restype = ctypes.c_int

        self.channel_num_recon = self.cal_file.channelNumChange
        self.channel_num_recon.restype = ctypes.c_int

        self.filt = self.cal_file.splitPack2Filter
        self.filt.restype = ctypes.POINTER(ctypes.c_int)

        self.recv_res = self.cal_file.resultReturn
        self.recv_res.restype = ctypes.POINTER(ctypes.c_double)

    def filter_init(self):
        config_init = configparser.ConfigParser()
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_init = os.path.join(myFolder, os.path.pardir, '.temp', '.config.ini')
        config_init.read(file_config_init)
        config_init_filter = config_init['Filter']
        sampling_freq = int(config_init_filter['sampling_freq'])
        INPUT = ctypes.c_double*30
        if int(config_init_filter['filter_notch_able']):
            filter_cache_a = []
            filter_cache_b = []

            if int(config_init_filter['filter_notch']) == 50:
                filter_cache_a = (sampling_freq // 50 + 1)*[0]
                filter_cache_b = (sampling_freq // 50 + 1)*[0]
                filter_cache_a[0] = 1
                filter_cache_a[-1] = -0.965081805687581
                filter_cache_b[0] = 0.98254090284379
                filter_cache_b[-1] = -0.98254090284379
                list_func = [self.filt_recon_comb, self.filt_recon_notch]
            else:
                [filter_cache_b, filter_cache_a] = sg.butter(3, [118 / sampling_freq, 122 / sampling_freq], 'bandstop')
                list_func = [self.filt_recon_notch, self.filt_recon_comb]
            length = len(filter_cache_a)
            data_a = INPUT()
            data_b = INPUT()
            for i in range(length):
                data_a[i] = filter_cache_a[i]
                data_b[i] = filter_cache_b[i]

            list_func[0](data_a, data_b, length)
            list_func[1](INPUT(), INPUT(), 0)
        else:
            self.filt_recon_comb(INPUT(), INPUT(), 0)
            self.filt_recon_notch(INPUT(), INPUT(), 0)

        if int(config_init_filter['filter_band_able']):
            low = 2*int(config_init_filter['filter_band_high']) / sampling_freq
            high = 2*int(config_init_filter['filter_band_low']) / sampling_freq
            [filter_cache_b, filter_cache_a] = sg.butter(7, [low, high], 'bandpass')
            length = len(filter_cache_a)
            data_a = INPUT()
            data_b = INPUT()
            for i in range(length):
                data_a[i] = filter_cache_a[i]
                data_b[i] = filter_cache_b[i]
            self.filt_recon_bandpass(data_a, data_b, length)
        else:
            self.filt_recon_bandpass(INPUT(), INPUT(), 0)

        self.channel_num_recon(int(config_init['Data']['channel_num']))

    def filter(self, cache):
        self.data2c += cache
        res = self.filt(self.data2c, len(self.data2c))
        for i in range(2):
            num, cost = res[0], res[1]
        res = []
        for i in range(num):
            temp_res = self.recv_res(i)
            temp = []
            for j in range(self.channel_num):
                temp.append(temp_res[j])
            res.append(temp)
        self.data2c = self.data2c[cost:]
        return np.array(res)

if __name__ == '__main__':
    cal = Cal()
    cal.filter_init()
    cal.filter(b'sfios_s')
