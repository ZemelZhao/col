#!/usr/bin/env python3
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox,
                             QGridLayout, QLCDNumber, QScrollArea)
import sys
import os
myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(myFolder, os.pardir, 'base'))
import pyqtgraph as pg
from widget import CustomAxis
from base import PlotWidgetCol
import time

___Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowGraphShow(QWidget):
    def __init__(self):
        super(WindowGraphShow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Graph')
        self.setFixedSize(1000, 800)

        layout_main = QHBoxLayout(self)
        layout_control = QVBoxLayout()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        """# layout_scroll"""
        layout_scroll = QHBoxLayout()
        self.scroll_area_widget = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_area_widget)

        layout_scroll_area = QHBoxLayout()
        self.graph_show = PlotWidgetCol()
        layout_scroll_area.addWidget(self.graph_show)
        self.scroll_area_widget.setLayout(layout_scroll_area)

        layout_scroll.addWidget(self.scroll_area)

        """# layout_control"""
        self.lcdnumber_countdown = QLCDNumber()
        self.lcdnumber_countdown.setDigitCount(4)
        self.lcdnumber_countdown.setMode(QLCDNumber.Dec)
        self.lcdnumber_countdown.setSegmentStyle(QLCDNumber.Flat)
        self.lcdnumber_countdown.setStyleSheet("""
                                               QLCDNumber{
                                               min-width: 150px;
                                               max-width: 150px;
                                               min-height: 80px;
                                               max-height: 80px;
                                               }
                                               """)
        self.lcdnumber_countdown_num = QLCDNumber()
        self.lcdnumber_countdown_num.setDigitCount(4)
        self.lcdnumber_countdown_num.setMode(QLCDNumber.Dec)
        self.lcdnumber_countdown_num.setSegmentStyle(QLCDNumber.Flat)
        self.lcdnumber_countdown_num.setStyleSheet("""
                                               QLCDNumber{
                                               min-width: 150px;
                                               max-width: 150px;
                                               min-height: 80px;
                                               max-height: 80px;
                                               }
                                               """)
        self.pushbutton_graph_save = QPushButton("Save Picture")
        self.pushbutton_graph_save.setStyleSheet("""
                                                 QPushButton{
                                                 min-width: 150px;
                                                 min-height: 60px;
                                                 }
                                                 """)

        self.pushbutton_data_save = QPushButton("Save Data")
        self.pushbutton_data_save.setStyleSheet("""
                                                 QPushButton{
                                                 min-width: 150px;
                                                 min-height: 60px;
                                                 }
                                                 """)

        widget = QWidget()
        widget.setMinimumSize(20, 300)

        layout_control.addWidget(widget)
        layout_control.addWidget(self.lcdnumber_countdown)
        layout_control.addWidget(self.lcdnumber_countdown_num)
        layout_control.addWidget(widget)
        layout_control.addWidget(self.pushbutton_data_save)
        layout_control.addWidget(self.pushbutton_graph_save)


        layout_main.addLayout(layout_scroll)
        layout_main.addLayout(layout_control)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowGraphShow()
    win.show()
    sys.exit(app.exec_())

