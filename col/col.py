#!/usr/bin/env python3

import sys
import os
import configparser
import shutil
import multiprocessing as mp
from windows.window_main import WindowMain
from logic.window_graph_show_logic import *
from logic.window_setting_logic import *
from logic.window_tinker_logic import *
from logic.head import Cal
from base.global_val import GlobalValue
import ctypes
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class MainWindow(WindowMain):
    def __init__(self, data_global, daemon_main, daemon_tcp_com, status_tcp_com):
        self.initial_setting()
        self.daemon_self = daemon_main
        self.daemon_tcp_com = daemon_tcp_com
        self.status_tcp_com = status_tcp_com
        self.data_global = data_global
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
        self.daemon_self.value = False

    def main_option(self):
        self.window_main_option = WindowOptionLogic(self)
        self.window_main_option.show()

    def graph_show(self):
        self.window_main_graph = WindowGraphShowLogic(self)
        self.window_main_graph.show()

    def prog_about(self):
        self.window_prog_about = WindowAboutLogic(self)
        self.window_prog_about.show()

    def prog_help(self):
        self.window_prog_help = WindowHelpLogic(self)
        self.window_prog_help.show()



class MainCom(mp.Process):
    def __init__(self, data_global, daemon_main, daemon_self, status_self):
        super(MainCom, self).__init__()
        self.data_global = data_global
        self.daemon_main = daemon_main
        self.daemon_self = daemon_self
        self.status_self = status_self
        self.first_judge = True
        pass

    def run(self):
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        file_config_ini = os.path.join(myFolder, '.temp', '.config.ini')
        while self.daemon_main.value:
            time.sleep(0.3)
            while self.daemon_self.value:
                if self.first_judge:
                    self.first_judge = False
                print('hello world')

class ProcessMonitor(mp.Process):
    def __init__(self):
        super(ProcessMonitor, self).__init__()

    def run(self):
        pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    daemon_main = mp.Value('b', True)
    daemon_tcp_com = mp.Value('b', False)
    status_tcp_com = mp.Value('b', False)
    data_global = GlobalValue()
    com = MainCom(data_global, daemon_main, daemon_tcp_com, status_tcp_com)
    mon = ProcessMonitor()
    app = QApplication(sys.argv)
    win = MainWindow(data_global, daemon_main, daemon_tcp_com, status_tcp_com)
    win.show()
    com.start()
    mon.start()
    sys.exit(app.exec_())


