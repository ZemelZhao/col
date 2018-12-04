#!/usr/bin/env python3

import sys
import os
import shutil
import configparser
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.path.pardir))
from windows.window_graph_show_all import WindowGraphShow
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
    def __init__(self):
        super(WindowGraphShowLogic, self).__init__()
        self.graph_show.setRange(yRange=[10, 192], padding=0)
        self.graph_show.enableAutoRange(y=1.0)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowGraphShowLogic()
    win.show()
    sys.exit(app.exec_())

