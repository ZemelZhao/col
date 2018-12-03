#!/usr/bin/env python3

import sys
import os
import shutil
import configparser
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from windows.window_graph_show import WindowGraphShow
from PyQt5.QtCore import pyqtSignal, QObject

import pyqtgraph as pg
import os
import pyqtgraph.exporters as ep
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.pardir, 'base'))
from widget import CustomAxis
from global_val import GlobalValue
#pg.setConfigOption('crashWarning', True)

import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowGraphShowLogic(WindowGraphShow):
    def __init__(self, parent=None, dir_save=None, data_global=None):
        self.parent = parent
        if self.parent == None:
            self.myFolder = os.path.split(os.path.realpath(__file__))[0]
            self.path_temp = os.path.join(self.myFolder, os.pardir, '.temp')
            self.path_config = os.path.join(self.myFolder, os.pardir, 'config')
            files = os.listdir(self.path_temp)
            if files:
                pass
            else:
                shutil.copy(os.path.join(self.path_config, 'config.ini'), os.path.join(self.path_temp, '.config.ini'))
                shutil.copy(os.path.join(self.path_config, 'info.ini'), os.path.join(self.path_temp, '.info.ini'))
        super(WindowGraphShowLogic, self).__init__()
        self.checkbox_clickedable = True
        self.dir_save = dir_save
        self.data_global = data_global

    def initUI(self):
        self.config_ini_read()
        self.judge_close = False
        super(WindowGraphShowLogic, self).initUI()
        self.display_initial()
        for i in self.list_checkbox_channel:
            i.stateChanged.connect(self.action_checkbox_channel_choose)
        self.pushbutton_custom_select_num.clicked.connect(self.action_pushbutton_custom_select_num)
        self.pushbutton_graph_save.clicked.connect(self.action_pushbutton_graph_save)

    def config_ini_read(self):
        config_ini = configparser.ConfigParser()
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_ini = os.path.join(myFolder, os.path.pardir, '.temp', '.config.ini')
        config_ini.read(file_config_ini)
        self.channel_num = int(config_ini['Data']['channel_num']) // 64

    def display_initial(self):
        for i in range(self.channel_num*64):
            self.list_checkbox_channel[i].setEnabled(True)
        for i in range(self.channel_num*64, 192):
            self.list_checkbox_channel[i].setEnabled(False)


        cache_label = [(i, str(i + 100)) for i in range(1, 193)]

        x = 80*np.random.normal(size=1000)
        y = 80*np.random.normal(size=1000)

        for i in range(self.channel_num * 2):
            self.list_graph_show[i].setRange(yRange=[32*i + 2, 32*(i + 1)])
            self.list_graph_show[i].plot(x, y)
        for i in range(self.channel_num*2, 6):
            img = pg.ImageItem(255*np.random.normal(1, size=(666, 666)))
            self.list_graph_show[i].setTitle('No such Channels')
            self.list_graph_show[i].addItem(img)
        self.list_graph_show[-1].setRange(yRange=[2, 32])

    def action_pushbutton_custom_select_num(self):
        self.data_lineedit_check()
        num, cache = self.cal_num_channel_choose(1)
        if num > 32:
            self.action_checkbox_channel_choose()
        else:
            for i in range(self.channel_num*64):
                if i in cache:
                    self.list_checkbox_channel[i].setChecked(True)
                else:
                    self.list_checkbox_channel[i].setChecked(False)
        temp_data_lineedit_custom_select_num = self.lineedit_custom_select_num.text()
        cache_select_num = temp_data_lineedit_custom_select_num.split('-')

    def action_checkbox_channel_choose(self):
        num, cache = self.cal_num_channel_choose(0)
        if num >= 32:
            if num == 32:
                for i in range(64*self.channel_num):
                    self.list_checkbox_channel[i].setEnabled(True)
                cache = [(hex(i)[2:].upper()).zfill(16) for i in cache]
                data_lineedit = '%16s-%16s-%16s' % (cache[0], cache[1], cache[2])
                self.lineedit_custom_select_num.setText(data_lineedit)
            else:
                num, cache = self.cal_num_channel_choose(1)
                for i in range(self.channel_num*64):
                    if i in cache:
                        self.list_checkbox_channel[i].setChecked(True)
                    else:
                        self.list_checkbox_channel[i].setChecked(False)
                num = 32
            self.checkbox_clickedable = False
            for i in range(64*self.channel_num):
                self.list_checkbox_channel[i].setEnabled(self.list_checkbox_channel[i].isChecked())
        else:
            if self.checkbox_clickedable == False:
                self.checkbox_clickedable = True
                for i in range(64*self.channel_num):
                    self.list_checkbox_channel[i].setEnabled(True)
            cache = [(hex(i)[2:].upper()).zfill(16) for i in cache]
            data_lineedit = '%16s-%16s-%16s' % (cache[0], cache[1], cache[2])
            self.lineedit_custom_select_num.setText(data_lineedit)
        self.label_custom_select_num.setText('%02d / 32' % num)

    def cal_num_channel_choose(self, mode=0):
        cache = []
        if mode:
            temp_data_lineedit_custom_select_num = self.lineedit_custom_select_num.text()
            cache_select_num = temp_data_lineedit_custom_select_num.split('-')
            for i in range(self.channel_num):
                temp_data = int(cache_select_num[i], 16)
                for j in range(64):
                    if temp_data >> j & 1:
                        cache.append(i*64 + j)
            return len(cache), cache
        else:
            res = 0
            for i in range(self.channel_num):
                temp = 0
                for j in range(64):
                    if self.list_checkbox_channel[i*64 + j].isChecked():
                        res += 1
                        temp += 1 << j
                cache.append(temp)
            for i in range(3 - self.channel_num):
                cache.append(0)
            return res, cache

    def data_lineedit_check(self):
        cache_temp = self.lineedit_custom_select_num.text().split('-')
        if len(cache_temp) == 3:
            for i in range(3):
                try:
                    data_temp = int(cache_temp[i], 16)
                    cache_temp[i] = data_temp
                except ValueError:
                    cache_temp[i] = 0
                    data_temp = 0
                finally:
                    if data_temp > 18446744073709551615:
                        cache_temp[i] = 0
        else:
            cache_temp = [0, 0, 0]
        cache = [(hex(i)[2:].upper()).zfill(16) for i in cache_temp]
        data_lineedit = '%16s-%16s-%16s' % (cache[0], cache[1], cache[2])
        self.lineedit_custom_select_num.setText(data_lineedit)

    def action_pushbutton_graph_save(self, e):
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        dict_list_channel = {'001 - 032': 0,
                             '033 - 064': 1,
                             '065 - 096': 2,
                             '097 - 128': 3,
                             '129 - 160': 4,
                             '161 - 192': 5,
                             'Custom': 6}

        exporter = ep.ImageExporter(self.list_graph_show[dict_list_channel[
            self.list_channel.currentItem().text()]].plotItem)
        if exporter.parameters()['height'] < 800:
            exporter.parameters()['height'] = 800
        exporter.export(os.path.join(myFolder, os.path.pardir, 'save', self.dir_save, 'temp%d.png'% self.data_global.draw_save_global))
        self.data_global.draw_save_global += 1

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowGraphShowLogic()
    win.show()
    sys.exit(app.exec_())

