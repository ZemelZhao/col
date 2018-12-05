#!/usr/bin/env python3

import sys
import os
import shutil
import configparser
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from windows.window_graph_show_all import WindowGraphShow
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

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
        super(WindowGraphShowLogic, self).__init__()
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


    def initUI(self):
        super(WindowGraphShowLogic, self).initUI()
        self.config_ini_read()
        myFolder = os.path.split(os.path.realpath(__file__))[0]

        self.scroll_area_widget.setMinimumSize(798, self.channel_num*12)
        self.graph_show.setRange(yRange=[0.3, self.channel_num+0.7], xRange=(-0.2, 10.2), padding=0)
        axis_y = self.graph_show.getAxis('left')
        ticks = range(1, self.channel_num+1)
        axis_y.setTicks([[(i, str(i)) for i in ticks]])
        self.graph_show.invertY()
        for i in range(self.channel_num+1):
            self.graph_show.addLine(y=i+0.5, pen='k')
        for i in range(1, 11):
            self.graph_show.addLine(x=i, pen='k')

    def config_ini_read(self):
        config_ini = configparser.ConfigParser()
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_ini = os.path.join(myFolder, os.path.pardir, '.temp', '.config.ini')
        config_ini.read(file_config_ini)
        self.channel_num = int(config_ini['Data']['channel_num'])


    @pyqtSlot(bool)
    def pic_update(self, e):
        pass



if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowGraphShowLogic()
    win.show()
    sys.exit(app.exec_())

