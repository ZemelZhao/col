#!/usr/bin/env python3

import sys
import os
import configparser
import shutil
from windows.window_main import WindowMain
from logic.window_graph_show_logic import *
from logic.window_setting_logic import *
from logic.window_tinker_logic import *
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class Main(WindowMain):
    def __init__(self):
        self.initial_setting()
        super(Main, self).__init__()

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

    def main_option(self):
        self.window_main_option = WindowOptionLogic(self)
        self.window_main_option.show()

    def graph_show(self):
        self.window_main_graph = WindowGraphShowLogic(self)
        self.window_main_graph.show()

    def prog_about(self):
        self.window_prog_about = WindowAboutLogic(self)
        self.window_prog_about.show()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())


