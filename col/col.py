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
import ctypes
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class MainWindow(WindowMain):
    def __init__(self, daemon):
        self.initial_setting()
        self.daemon = daemon
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
        self.daemon.value = False

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
    def __init__(self, daemon):
        super(MainCom, self).__init__()
        self.daemon = daemon
        pass

    def run(self):
        while self.daemon.value:
            print('hello world')
            time.sleep(0.5)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    daemon = mp.Value('b', True)
    com = MainCom(daemon)
    app = QApplication(sys.argv)
    win = MainWindow(daemon)
    win.show()
    com.start()
    sys.exit(app.exec_())


