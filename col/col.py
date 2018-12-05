#!/usr/bin/env python3

import sys
import os
import configparser
import shutil
import multiprocessing as mp
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from windows.window_main import WindowMain
from logic.window_graph_show_all_logic import *
from logic.window_setting_logic import *
from logic.window_tinker_logic import *
from logic.head import Cal
from base.global_val import GlobalValue
import pyqtgraph.exporters as ep
import ctypes
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class MainWindow(WindowMain):
    state = pyqtSignal(bool)
    def __init__(self, data_global, daemon_main, daemon_tcp_com, status_tcp_com):
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.initial_setting()
        self.daemon_self = daemon_main
        self.daemon_tcp_com = daemon_tcp_com
        self.status_tcp_com = status_tcp_com
        self.data_global = data_global

        time_cache = time.localtime(time.time())
        self.dir_save = '%4d%02d%02d%02d%02d%02d' % (time_cache[0], time_cache[1], time_cache[2],
                                                       time_cache[3], time_cache[4], time_cache[5])
        self.dir_save = os.path.join(myFolder, 'save', self.dir_save)
        super(MainWindow, self).__init__()

    def initial_setting(self):
        self.myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.path_temp = os.path.join(self.myFolder, '.temp')
        self.path_config = os.path.join(self.myFolder, 'config')
        shutil.rmtree(self.path_temp)
        os.makedirs(self.path_temp)
        shutil.copy(os.path.join(self.path_config, 'config.ini'), os.path.join(self.path_temp, '.config.ini'))
        shutil.copy(os.path.join(self.path_config, 'info.ini'), os.path.join(self.path_temp, '.info.ini'))

    def closeEvent(self, item):
        self.path_temp = os.path.join(self.myFolder, '.temp')
        shutil.rmtree(self.path_temp)
        os.makedirs(self.path_temp)
        self.state.emit(False)
        self.daemon_self.value = False

    def main_option(self):
        self.window_main_option = WindowOptionLogic(self)
        self.state.connect(self.window_main_option.close)
        self.window_main_option.show()

    def graph_show(self):
        self.window_graph_show = WindowGraphShowLogic(self, self.dir_save, self.data_global)
        self.state.connect(self.window_graph_show.close)
        self.window_graph_show.show()

    def prog_about(self):
        self.window_prog_about = WindowAboutLogic()
        self.state.connect(self.window_prog_about.close)
        self.window_prog_about.show()

    def prog_help(self):
        self.window_prog_help = WindowHelpLogic(self)
        self.state.connect(self.window_prog_help.close)
        self.window_prog_help.show()

    def pic_save(self):
        if not self.window_graph_show.isClosed():
            if not os.path.exists(self.dir_save):
                os.mkdir(self.dir_save)
            dict_list_channel = {'001 - 032': 0,
                                 '033 - 064': 1,
                                 '065 - 096': 2,
                                 '097 - 128': 3,
                                 '129 - 160': 4,
                                 '161 - 192': 5,
                                 'Custom': 6}

            exporter = ep.ImageExporter(self.window_graph_show.list_graph_show[dict_list_channel[
                self.window_graph_show.list_channel.currentItem().text()]].plotItem)
            if exporter.parameters()['height'] < 800:
                exporter.parameters()['height'] = 800
            exporter.export(os.path.join(self.dir_save, 'temp%d.png'% self.data_global.draw_save_global))
            self.data_global.draw_save_global += 1

    pyqtSlot(int)
    def show_warning(self, e):
        if e == 0:
            QMessageBox.warning(self, 'Warning',
                                'TCP/IP cannot connected\n Please Check!',
                                QMessageBox.Ok)
        else:
            pass


class MainCom(QObject, mp.Process):
    state_tcp_ip = pyqtSignal(int)
    def __init__(self, data_global, daemon_main, daemon_self, status_self):
        super(MainCom, self).__init__()
        self.data_global = data_global
        self.daemon_main = daemon_main
        self.daemon_self = daemon_self
        self.status_self = status_self

    def run(self):
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_ini = os.path.join(myFolder, '.temp', '.config.ini')
        print('hello')
        while True:
            time.sleep(0.3)
            pass

    @pyqtSlot(bool)
    def closeSignalRec(self, e):
        if not e:
            self.terminate()

class ProcessMonitor(QObject, mp.Process):
    def __init__(self, daemon_main):
        super(ProcessMonitor, self).__init__()
        self.daemon_main = daemon_main

    def run(self):
        while True:
            pass

    @pyqtSlot(bool)
    def closeSignalRec(self, e):
        if not e:
            self.terminate()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    daemon_main = mp.Value('b', True)
    daemon_tcp_com = mp.Value('b', False)
    status_tcp_com = mp.Value('b', False)
    data_global = GlobalValue()
    com = MainCom(data_global, daemon_main, daemon_tcp_com, status_tcp_com)
    mon = ProcessMonitor(daemon_main)
    app = QApplication(sys.argv)
    win = MainWindow(data_global, daemon_main, daemon_tcp_com, status_tcp_com)
    win.state.connect(com.closeSignalRec)
    win.state.connect(mon.closeSignalRec)
    com.state_tcp_ip.connect(win.show_warning)

    win.show()
    com.start()
    mon.start()
    sys.exit(app.exec_())


