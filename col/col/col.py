#!/usr/bin/env python3

import sys
import os
import configparser
import shutil
import multiprocessing as mp
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QMdiSubWindow
from PyQt5.QtGui import QCloseEvent
from windows.window_main import WindowMain
from logic.window_graph_show_all_logic import *
from logic.window_setting_logic import *
from logic.window_tinker_logic import *
from logic.head import Cal
from base.gui_val import GUIValue
import pyqtgraph.exporters as ep
import ctypes
import numpy as np
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class MainWindow(WindowMain):
    signal_state = pyqtSignal(QCloseEvent)
    signal_config_refresh = pyqtSignal(bool)
    signal_pic_save = pyqtSignal([pg.graphicsItems.PlotItem.PlotItem, str])

    def __init__(self, shared_data_graph):
        super(MainWindow, self).__init__()
        self.myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.data_global = GUIValue()

        time_cache = time.localtime(time.time())
        self.dir_save = '%4d%02d%02d%02d%02d%02d' % (time_cache[0], time_cache[1], time_cache[2],
                                                       time_cache[3], time_cache[4], time_cache[5])
        self.dir_save = os.path.join(self.myFolder, 'save', self.dir_save)
        self.shared_data_graph = shared_data_graph
        self.window_graph_show = WindowGraphShowLogic(shared_data_graph = self.shared_data_graph)
        self.initial_setting()

    def initial_setting(self):
        self.myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.path_temp = os.path.join(self.myFolder, '.temp')
        self.path_config = os.path.join(self.myFolder, 'config')
        shutil.rmtree(self.path_temp)
        os.makedirs(self.path_temp)
        shutil.copy(os.path.join(self.path_config, 'config.ini'), os.path.join(self.path_temp, '.config.ini'))
        shutil.copy(os.path.join(self.path_config, 'info.ini'), os.path.join(self.path_temp, '.info.ini'))
        self.slot_refresh_config()

    def closeEvent(self, item):
        self.path_temp = os.path.join(self.myFolder, '.temp')
        shutil.rmtree(self.path_temp)
        os.makedirs(self.path_temp)
        self.signal_state.emit(item)

    def main_option(self):
        self.window_main_option = WindowOptionLogic(self)
        self.signal_state.connect(self.window_main_option.close)
        self.window_main_option.pushbutton_ok_page1.clicked.connect(self.slot_refresh_config)
        self.window_main_option.show()

    def graph_show(self):
        if self.window_graph_show.isClosed():
            self.window_graph_show = WindowGraphShowLogic(self, self.dir_save, self.shared_data_graph)
            self.window_graph_show.startTimer()
            sub = QMdiSubWindow()
            sub.setWidget(self.window_graph_show)
            self.mdi.addSubWindow(sub)
            self.signal_config_refresh.connect(self.window_graph_show.updata_config)
            self.window_graph_show.signal_pic_save.connect(self.pic_save)
            self.window_graph_show.show()

    def prog_about(self):
        self.window_prog_about = WindowAboutLogic()
        self.signal_state.connect(self.window_prog_about.close)
        self.window_prog_about.show()

    def prog_help(self):
        self.window_prog_help = WindowHelpLogic(self)
        self.signal_state.connect(self.window_prog_help.close)
        self.window_prog_help.show()

    def pic_save(self):
        if not self.window_graph_show.isClosed():
            if not os.path.exists(self.dir_save):
                os.mkdir(self.dir_save)
            self.signal_pic_save.emit(self.window_graph_show.graph_show, self.dir_save)

    @pyqtSlot(int)
    def show_warning(self, e):
        if e == 0:
            QMessageBox.warning(self, 'Warning',
                                'TCP/IP cannot connected\n Please Check!',
                                QMessageBox.Ok)
        else:
            pass

    def slot_refresh_config(self):
        config_ini = configparser.ConfigParser()
        file_config_ini = os.path.join(self.myFolder, '.temp', '.config.ini')
        config_ini.read(file_config_ini)
        self.channel_num = int(config_ini['Data']['channel_num'])
        self.signal_config_refresh.emit(True)


    @pyqtSlot(str)
    def slot_status_bar_changed(self, e):
        self.statusBar().showMessage(e)


class MainCom(QObject, mp.Process):
    state_tcp_ip = pyqtSignal(int)
    def __init__(self, shared_data_graph, status_change):
        super(MainCom, self).__init__()
        self.shared_data_graph = shared_data_graph
        self.not_change  = status_change

    def run(self):
        data_clear = 192*1000*[0]
        while True:
            time.sleep(0.01)
            config_ini = configparser.ConfigParser()
            myFolder = os.path.split(os.path.realpath(__file__))[0]
            file_config_ini = os.path.join(myFolder, '.temp', '.config.ini')
            config_ini.read(file_config_ini)
            channel_num = int(config_ini['Data']['channel_num'])
            self.shared_data_graph[:] = data_clear[:]
            self.not_change.value = True
            while self.not_change.value:
                if not self.not_change.value:
                    break
                num_data = 20
                graph_data = 1000
                num_change = channel_num*num_data
                num_all = channel_num*graph_data
                self.shared_data_graph[:num_all-num_change] = self.shared_data_graph[num_change:num_all]
                data = np.random.normal(size=(channel_num, num_data)).reshape(1, -1)
                self.shared_data_graph[num_all-num_change:num_all] = data[0][:]
                time.sleep(0.2)

    def statusChange(self):
        self.not_change.value = False

    def closeEvent(self, e):
        self.terminate()

class ProcessMonitor(QObject, mp.Process):
    def __init__(self):
        super(ProcessMonitor, self).__init__()

    def run(self):
        while True:
            pass

    def closeEvent(self, e):
        self.terminate()

class ProcessSave(QObject, mp.Process):
    signal_state_save = pyqtSignal(str)
    def __init__(self):
        super(ProcessSave, self).__init__()
        self.list_action = []
        self.graph_no = 0

    def run(self):
        while True:
            if self.list_action:
                pass
            else:
                time.sleep(0.2)


    def closeEvent(self, e):
        self.terminate()

    @pyqtSlot(pg.graphicsItems.PlotItem.PlotItem, str)
    def save_pic(self, e0, e1):
        try:
            exporter = ep.ImageExporter(e0.plotItem)
            if exporter.parameters()['height'] < 800:
                exporter.parameters()['height'] = 800
            exporter.export(os.path.join(e1, 'temp%d.png'% self.graph_no))
            self.graph_no += 1
            self.signal_state_save.emit('Picture Saved Successfully')
        except:
            self.signal_state_save.emit('Picture Saved Failed')
        finally:
            pass

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    shared_data_graph = mp.Array('d', np.array(192*1000*[0]))
    shared_config_change = mp.Value('b', False)

    com = MainCom(shared_data_graph, shared_config_change)
    mon = ProcessMonitor()
    sav = ProcessSave()
    app = QApplication(sys.argv)
    win = MainWindow(shared_data_graph)

    win.signal_state.connect(com.closeEvent)
    win.signal_state.connect(mon.closeEvent)
    win.signal_state.connect(sav.closeEvent)
    win.signal_pic_save.connect(sav.save_pic)
    win.signal_config_refresh.connect(com.statusChange)
    com.state_tcp_ip.connect(win.show_warning)
    sav.signal_state_save.connect(win.slot_status_bar_changed)

    win.show()
    com.start()
    mon.start()
    sav.start()
    sys.exit(app.exec_())
