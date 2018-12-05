#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox,
                             QGridLayout, QLCDNumber, QMainWindow, QAction,
                             QMessageBox, QMdiArea, QMdiSubWindow)
import os
import sys
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(myFolder)

from .window_setting import WindowOption
from .window_graph_show_all import WindowGraphShow
from .window_tinker import WindowAbout, WindowHelp
import os
import pyqtgraph as pg
import time

class WindowMain(QMainWindow):
    def __init__(self):
        super(WindowMain, self).__init__()
        self.window_main_option = WindowOption()
        self.window_graph_show = WindowGraphShow()
        self.window_prog_about = WindowAbout()
        self.window_prog_help = WindowHelp()
        self.initUI()

    def initUI(self):
        self.resize(1100, 900)
        self.setWindowTitle('Main')
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.path_resource = os.path.join(myFolder, os.pardir, 'resource')

        """# Action"""
        icon_filesave = os.path.join(self.path_resource, 'filesave')
        icon_picsave = os.path.join(self.path_resource, 'picsave')
        icon_option = os.path.join(self.path_resource, 'option')
        icon_graph = os.path.join(self.path_resource, 'graph')
        icon_start = os.path.join(self.path_resource, 'start')
        icon_help = os.path.join(self.path_resource, 'help')
        icon_info = os.path.join(self.path_resource, 'info')
        self.action_option = self.create_action('&Option', self.main_option, 'Ctrl + O', icon_option, None)
        self.action_graph = self.create_action('&Graph', self.graph_show, 'Ctrl + G', icon_graph, None)
        self.action_about = self.create_action('About', self.prog_about, None, icon_info, None)
        self.action_help = self.create_action('Help', self.prog_help, None, icon_help, None)
        self.action_start = self.create_action('Start/Restart', self.start_restart, None, icon_start, None)
        self.action_filesave = self.create_action('filesave', self.file_save, None, icon_filesave, None)
        self.action_picsave = self.create_action('picsave', self.pic_save, None, icon_picsave, None)

        """# Menu Bar"""
        menu_file = self.menuBar().addMenu('&File')
        menu_show = self.menuBar().addMenu('&Graph')
        menu_advanced = self.menuBar().addMenu('&Advanced')
        menu_help = self.menuBar().addMenu('&Help')

        self.add_actions(menu_file, [self.action_option])
        self.add_actions(menu_show, [self.action_graph])
        self.add_actions(menu_help, [self.action_about])

        """# Tool Bar"""
        self.toolbar_main_option = self.addToolBar('Option')
        self.toolbar_main_option.addAction(self.action_option)
        self.toolbar_main_option.addAction(self.action_graph)

        self.toolbar_main_control = self.addToolBar('Control')
        self.toolbar_main_control.addAction(self.action_start)
        self.toolbar_main_control.addAction(self.action_filesave)
        self.toolbar_main_control.addAction(self.action_picsave)

        self.toolbar_tinker = self.addToolBar('Tinker')
        self.toolbar_tinker.addAction(self.action_help)
        self.toolbar_tinker.addAction(self.action_about)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

    def main_option(self):
        self.window_main_option.show()

    def graph_show(self):
        sub = QMdiSubWindow()
        sub.setWidget(self.window_graph_show)
        self.mdi.addSubWindow(sub)
        self.window_graph_show.show()

    def prog_about(self):
        self.window_prog_about.show()

    def prog_help(self):
        self.window_prog_help.show()

    def start_restart(self):
        pass

    def file_save(self):
        pass

    def pic_save(self):
        pass


    def create_action(self, text, slot=None, shortcut=None, icon=None,
                      tip=None, checkable=None, signal='triggered()'):
        action = QAction(text, self)
        if slot is not None:
            action.triggered.connect(slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(QIcon('%s.png'%icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable is not None:
            action.setCheckable(True)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowMain()
    win.show()
    sys.exit(app.exec_())

