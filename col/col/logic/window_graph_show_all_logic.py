#!/usr/bin/env python3

import sys
import os
import shutil
import configparser
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from windows.window_graph_show_all import WindowGraphShow
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer

import pyqtgraph as pg
import os
import pyqtgraph.exporters as ep
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.pardir, 'base'))
from widget import CustomAxis
from gui_val import GUIValue
#pg.setConfigOption('crashWarning', True)

import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowGraphShowLogic(WindowGraphShow):
    signal_pic_save = pyqtSignal(bool)
    signal_set_done = pyqtSignal(bool)
    def __init__(self, parent=None, dir_save=None, shared_data_graph=None):
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
        self.judge_close = True
        self.shared_data_graph = shared_data_graph
        self.timer_graph  = QTimer()
        self.timer_lcd = QTimer()
        self.timer_graph.timeout.connect(self.update_graph)
        self.timer_lcd.timeout.connect(self.update_lcd)
        self.lcd_shown = False
        super(WindowGraphShowLogic, self).__init__()

    def show(self, *arg, **kwarg):
        self.judge_close = False
        super(WindowGraphShowLogic, self).show(*arg, **kwarg)

    def initUI(self):
        super(WindowGraphShowLogic, self).initUI()
        self.updata_config()
        self.pushbutton_graph_save.clicked.connect(self.graph_save)
        self.pushbutton_data_save.clicked.connect(self.data_save)

    def config_ini_read(self):
        config_ini = configparser.ConfigParser()
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_ini = os.path.join(myFolder, os.path.pardir, '.temp', '.config.ini')
        config_ini.read(file_config_ini)
        config_data = config_ini['Data']
        self.channel_num = int(config_data['channel_num'])
        self.restart_auto = int(config_data['auto_res_able'])
        self.restart_time = int(config_data['auto_res_time'])
        self.period_time = int(config_data['set_time'])
        self.set_number = int(config_data['set_number'])
        self.train_pass_all = self.period_time + (self.set_number - 1)*(self.period_time + self.restart_time)
        self.time_period = self.period_time + self.restart_time

    def isClosed(self):
        return self.judge_close

    def closeEvent(self, e):
        self.judge_close = True
        self.stopTimer()
        super(WindowGraphShow, self).closeEvent(e)

    def graph_save(self):
        self.signal_pic_save.emit(True)

    def data_save(self):
        pass

    def update_graph(self):
        data = np.frombuffer(self.shared_data_graph.get_obj())
        data = data.reshape(-1, self.channel_num).T
        x_data = np.array(1000)
        for i in range(self.channel_num):
            self.list_curve[i].setData(y=data[i, :1000] + i + 1, pen=(0, 0, 0))

    def update_lcd(self):
        self.lcdnumber_countdown.display(self.lcd_time_show)
        self.lcdnumber_countdown_num.display(self.lcd_num_show)

    def startTimer(self, e):
        if e:
            self.timer_lcd.start(100)
        else:
            self.timer_graph.start(1000)

    def stopTimer(self):
        self.timer_graph.stop()
        self.timer_lcd.stop()

    def lcd_control(self):
        if self.restart_auto:
            if self.lcd_shown:
                pass
            else:
                self.time_start = time.time()
                self.lcd_shown = True
            time_pass = time.time() - self.time_start
            if time_pass > self.time_pass_all:
                self.lcd_time_show = int(time_pass - self.time_pass_all)
                self.lcd_num_show = 0
            else:
                time_pass = int(time_pass)
                lcd_time = (time_pass) % self.time_period
                if lcd_time > self.period_time:
                    self.lcd_time_show = lcd_time - self.period_time
                else:
                    self.lcd_time_show = self.period_time - lcd_time
                self.lcd_num_show = (time_pass) // self.time_period + 1
        else:
            if self.lcd_shown:
                pass
            else:
                self.time_start = time.time()
                self.lcd_shown = True
            time_pass = time.time() - self.time_start
            if time_pass > self.period_time:
                self.lcd_shown = False
                self.signal_set_done.emit(True)
                self.set_number -= 1
                self.lcd_time_show = 0
            else:
                self.lcd_time_show = self.period_time - time_pass
            self.lcd_num_show = self.set_number

    @pyqtSlot(bool)
    def updata_config(self, *arg):
        pointspersecond = 100
        show_time = 10
        self.config_ini_read()
        self.scroll_area_widget.setMinimumSize(798, self.channel_num*12)
        self.scroll_area_widget.setMaximumSize(798, self.channel_num*12)
        self.graph_show.setRange(yRange=[0.3, self.channel_num+0.7], xRange=(-0.01*pointspersecond, (show_time+0.1)*pointspersecond), padding=0)
        self.graph_show.clear()
        axis_x = self.graph_show.getAxis('bottom')
        axis_y = self.graph_show.getAxis('left')
        xticks = range(pointspersecond, show_time*pointspersecond + 1, pointspersecond)
        yticks = range(1, self.channel_num+1)
        axis_x.setTicks([[(i, str(i//pointspersecond)) for i in xticks]])
        axis_y.setTicks([[(i, str(i)) for i in yticks]])
        self.graph_show.invertY()
        for i in range(self.channel_num+1):
            self.graph_show.addLine(y=i+0.5, pen='k')
        for i in range(pointspersecond, show_time*pointspersecond, pointspersecond):
            self.graph_show.addLine(x=i, pen='k')
        self.list_curve = []
        for i in range(self.channel_num):
            self.list_curve.append(self.graph_show.plot())
            #self.list_curve[i].setDownsampling(mode='peak')
            self.list_curve[i].setClipToView(True)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    data_global = GUIValue()
    app = QApplication(sys.argv)
    win = WindowGraphShowLogic()
    win.show()
    sys.exit(app.exec_())

