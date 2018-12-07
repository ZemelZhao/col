#!/usr/bin/env python3

import sys
import os
import configparser
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from windows.window_setting import WindowOption

import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowOptionLogic(WindowOption):
    def __init__(self, parent=None):
        self.parent = parent
        self.cache_notch_filter = {50: 0, 60: 1}
        self.cache_bandpass_high = {1: 0, 5: 1, 10: 2, 20: 3}
        self.cache_bandpass_low = {50: 0, 100: 1, 200: 2, 450: 3}
        self.cache_sampling_freq = {250: 0, 500: 1, 1000: 2, 2000: 3}
        self.cache_channel_num = {64: 0, 128: 1, 192: 2}
        self.myFile = os.path.split(os.path.realpath(__file__))[0]
        super(WindowOptionLogic, self).__init__()

    def initUI(self):
        super(WindowOptionLogic, self).initUI()
        self.config_ini_read()
        self.pushbutton_ok_page0.clicked.connect(self.action_pushbutton_ok_page0)
        self.pushbutton_re_page0.clicked.connect(self.action_pushbutton_re_page0)
        self.pushbutton_de_page0.clicked.connect(self.action_pushbutton_de_page0)
        self.pushbutton_ok_page1.clicked.connect(self.action_pushbutton_ok_page1)
        self.pushbutton_re_page1.clicked.connect(self.action_pushbutton_re_page1)
        self.pushbutton_de_page1.clicked.connect(self.action_pushbutton_de_page1)
        self.pushbutton_reset_filter.clicked.connect(self.action_pushbutton_reset_filter)
        self.pushbutton_reset_data.clicked.connect(self.action_pushbutton_reset_data)
        self.pushbutton_reset_tcpip.clicked.connect(self.action_pushbutton_reset_tcpip)

        self.checkbox_notch_filter.stateChanged.connect(self.action_notch_filter_change)
        self.checkbox_bandpass_filter.stateChanged.connect(self.action_bandpass_filter_change)
        self.radiobutton_restart_auto.toggled.connect(self.action_auto_press_change)
        self.radiobutton_users_gender_secret_page1.setChecked(True)

        self.display_initial()

    def config_ini_read(self):
        config_ini = configparser.ConfigParser()
        config_res = configparser.ConfigParser()
        file_config_ini = os.path.join(self.myFile, os.path.pardir, '.temp', '.config.ini')
        file_config_res = os.path.join(self.myFile, os.path.pardir, 'config', 'config.ini')
        config_ini.read(file_config_ini)
        config_filter_data_ini = config_ini['Filter']
        config_filter_name_ini = config_ini.options('Filter')
        config_data_data_ini = config_ini['Data']
        config_data_name_ini = config_ini.options('Data')
        config_socket_data_ini = config_ini['Socket']
        config_socket_name_ini = config_ini.options('Socket')

        config_res.read(file_config_res)
        config_filter_data_res = config_res['Filter']
        config_filter_name_res = config_res.options('Filter')
        config_data_data_res = config_res['Data']
        config_data_name_res = config_res.options('Data')
        config_socket_data_res = config_res['Socket']
        config_socket_name_res = config_res.options('Socket')

        self.dict_config_filter_res = {}
        self.dict_config_data_res = {}
        self.dict_config_socket_res = {}

        self.dict_config_filter_ini = {}
        self.dict_config_data_ini = {}
        self.dict_config_socket_ini = {}

        for i in config_filter_name_ini:
            self.dict_config_filter_ini[i] = int(config_filter_data_ini[i])
            self.dict_config_filter_res[i] = int(config_filter_data_res[i])
        for i in config_data_name_ini:
            self.dict_config_data_ini[i] = int(config_data_data_ini[i])
            self.dict_config_data_res[i] = int(config_data_data_res[i])
        for i in config_socket_name_ini:
            self.dict_config_socket_ini[i] = config_socket_data_ini[i]
            self.dict_config_socket_res[i] = config_socket_data_res[i]

    def display_initial(self):
        self.checkbox_notch_filter.setChecked(self.dict_config_filter_ini['filter_notch_able'])
        self.checkbox_bandpass_filter.setChecked(self.dict_config_filter_ini['filter_band_able'])
        self.combobox_notch_filter.setCurrentIndex(self.cache_notch_filter[self.dict_config_filter_ini['filter_notch']])
        self.combobox_bandpass_high.setCurrentIndex(self.cache_bandpass_high[self.dict_config_filter_ini['filter_band_high']])
        self.combobox_bandpass_low.setCurrentIndex(self.cache_bandpass_low[self.dict_config_filter_ini['filter_band_low']])
        self.combobox_sampling_freq.setCurrentIndex(self.cache_sampling_freq[self.dict_config_filter_ini['sampling_freq']])

        self.combobox_channel_num.setCurrentIndex(self.cache_channel_num[self.dict_config_data_ini['channel_num']])
        self.spinbox_set_num.setValue(self.dict_config_data_ini['set_number'])
        self.spinbox_set_time.setValue(self.dict_config_data_ini['set_time'])
        self.spinbox_restart_auto.setValue(self.dict_config_data_ini['auto_res_time'])
        self.radiobutton_restart_auto.setChecked(self.dict_config_data_ini['auto_res_able'])
        self.radiobutton_restart_press.setChecked(not self.dict_config_data_ini['auto_res_able'])
        self.combobox_filetype_save.setCurrentIndex(self.dict_config_data_ini['filetype_save'])

        self.lineedit_tcp_address.setText(self.dict_config_socket_ini['tcp_address'])
        self.lineedit_tcp_port.setText(self.dict_config_socket_ini['tcp_port'])

        self.combobox_notch_filter.setEnabled(self.checkbox_notch_filter.isChecked())
        self.combobox_bandpass_high.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.combobox_bandpass_low.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.spinbox_restart_auto.setEnabled(self.radiobutton_restart_auto.isChecked())

    def action_pushbutton_ok_page0(self):
        self.close()

    def action_pushbutton_de_page0(self):
        self.close()

    def action_pushbutton_ok_page1(self):
        self.dict_config_filter_ini['filter_notch_able'] = str(int(self.checkbox_notch_filter.isChecked()))
        self.dict_config_filter_ini['filter_band_able'] = int(self.checkbox_bandpass_filter.isChecked())
        self.dict_config_filter_ini['filter_notch'] = int(self.combobox_notch_filter.currentText())
        self.dict_config_filter_ini['filter_band_high'] = int(self.combobox_bandpass_high.currentText())
        self.dict_config_filter_ini['filter_band_low'] = int(self.combobox_bandpass_low.currentText())
        self.dict_config_filter_ini['sampling_freq'] = int(self.combobox_sampling_freq.currentText())

        self.dict_config_data_ini['channel_num'] = int(self.combobox_channel_num.currentText())
        self.dict_config_data_ini['set_number'] = int(self.spinbox_set_num.value())
        self.dict_config_data_ini['set_time'] = int(self.spinbox_set_time.value())
        self.dict_config_data_ini['auto_res_able'] = int(self.radiobutton_restart_auto.isChecked())
        self.dict_config_data_ini['auto_res_time'] = int(self.spinbox_restart_auto.value())
        self.dict_config_data_ini['filetype_save'] = int(self.combobox_filetype_save.currentIndex())

        self.dict_config_socket_ini['tcp_address'] = self.lineedit_tcp_address.text()
        self.dict_config_socket_ini['tcp_port'] = self.lineedit_tcp_port.text()

        config_ini = configparser.ConfigParser()
        config_info = configparser.ConfigParser()

        file_config_ini = os.path.join(self.myFile, os.path.pardir, '.temp', '.config.ini')
        file_user_info = os.path.join(self.myFile, os.path.pardir, '.temp', '.info.ini')
        config_ini.read(file_config_ini)
        config_info.read(file_user_info)
        for i in self.dict_config_filter_ini.keys():
            config_ini.set('Filter', i, str(self.dict_config_filter_ini[i]))
        for i in self.dict_config_data_ini.keys():
            config_ini.set('Data', i, str(self.dict_config_data_ini[i]))
        for i in self.dict_config_socket_ini.keys():
            config_ini.set('Socket', i, str(self.dict_config_socket_ini[i]))
        config_ini.write(open(file_config_ini, 'w'))
        self.close()

    def action_pushbutton_de_page1(self):
        self.close()

    def action_pushbutton_re_page0(self):
        pass

    def action_pushbutton_re_page1(self):
        self.dict_config_filter_ini = self.dict_config_filter_res.copy()
        self.dict_config_data_ini = self.dict_config_data_res.copy()
        self.dict_config_socket_ini = self.dict_config_socket_res.copy()
        self.display_initial()

    def action_pushbutton_reset_filter(self):
        self.dict_config_filter_ini = self.dict_config_filter_res.copy()
        self.display_initial()

    def action_pushbutton_reset_data(self):
        self.dict_config_data_ini = self.dict_config_data_res.copy()
        self.display_initial()

    def action_pushbutton_reset_tcpip(self):
        self.dict_config_socket_ini = self.dict_config_socket_res.copy()
        self.display_initial()

    def action_notch_filter_change(self):
        self.combobox_notch_filter.setEnabled(self.checkbox_notch_filter.isChecked())

    def action_bandpass_filter_change(self):
        self.combobox_bandpass_high.setEnabled(self.checkbox_bandpass_filter.isChecked())
        self.combobox_bandpass_low.setEnabled(self.checkbox_bandpass_filter.isChecked())

    def action_auto_press_change(self):
        self.spinbox_restart_auto.setEnabled(self.radiobutton_restart_auto.isChecked())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowOptionLogic()
    win.show()
    sys.exit(app.exec_())
