#!/usr/bin/env python3
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox,
                             QGridLayout, QLCDNumber)
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
        self.judge_close = True
        self.initUI()

    def show(self):
        self.judge_close = False
        super(WindowGraphShow, self).show()

    def initUI(self):
        self.setWindowTitle('Graph')
        self.setFixedSize(1000, 800)

        self.list_channel = QListWidget(self)
        self.stack_window = QStackedWidget(self)
        self.channel_monitor = QWidget()
        self.graph_control = QWidget()

        layout_main = QHBoxLayout(spacing=0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        layout_main.addWidget(self.list_channel)
        layout_main.addWidget(self.stack_window)
        layout_main.addWidget(self.channel_monitor)
        layout_main.addWidget(self.graph_control)

        self.setLayout(layout_main)

        """# List Channel"""
        self.list_channel.setFrameShape(QListWidget.NoFrame)
        self.list_channel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_channel.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_channel.currentRowChanged.connect(self.stack_window.setCurrentIndex)

        self.list_channel.setStyleSheet("""
                                       QListWidget{
                                       min-width: 150px;
                                       max-width: 150px;
                                       color: white;
                                       background: grey;
                                       }
                                       """)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(20)

        for i in range(6):
            item = QListWidgetItem()
            item.setFont(font)
            item.setText('%03d - %03d' % (32*i + 1, 32*(i + 1)))
            item.setSizeHint(QSize(0, 60))
            item.setTextAlignment(Qt.AlignCenter)
            self.list_channel.addItem(item)
        item = QListWidgetItem()
        item.setFont(font)
        item.setText('Custom')
        item.setSizeHint(QSize(0, 60))
        item.setTextAlignment(Qt.AlignCenter)
        self.list_channel.addItem(item)

        """# Stack Window"""
        self.list_page_widget = []
        self.list_graph_show = []
        self.list_layout_page = []
        self.list_tabwidget = []

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        list_stringaxis = []

        for i in range(7):
            list_stringaxis.append(CustomAxis({1:'a', 2: 'b'}, orientation='left'))
            self.list_page_widget.append(QWidget())
            self.list_graph_show.append(PlotWidgetCol(axisItems={'left':list_stringaxis[i]}))
            self.list_layout_page.append(QHBoxLayout())
            self.list_layout_page[i].setContentsMargins(0, 0, 0, 0)
            self.list_tabwidget.append(QTabWidget())

        for i in range(7):
            self.list_page_widget[i].setLayout(self.list_layout_page[i])
            self.list_layout_page[i].addWidget(self.list_tabwidget[i])
            self.stack_window.addWidget(self.list_page_widget[i])
            tab_graph = QWidget()
            tab_monitor = QWidget()
            self.list_tabwidget[i].addTab(tab_graph, 'Graph')
            self.list_tabwidget[i].addTab(tab_monitor, 'Monitor')
            layout_page = QHBoxLayout()
            layout_graph = QHBoxLayout()
            layout_graph.addWidget(self.list_graph_show[i])
            tab_graph.setLayout(layout_graph)
            layout_monitor = QGridLayout()
            tab_monitor.setLayout(layout_monitor)

        tab_custom_option = QWidget()
        layout_tab_custom_option = QVBoxLayout()
        tab_custom_option.setLayout(layout_tab_custom_option)
        self.list_tabwidget[6].addTab(tab_custom_option, 'Select')

        """# Page Custom Tab Select"""
        layout_tab_custom_option_up = QHBoxLayout()
        layout_tab_custom_option_mid = QHBoxLayout()
        layout_tab_custom_option_down = QHBoxLayout()
        layout_tab_custom_option.addLayout(layout_tab_custom_option_up)
        layout_tab_custom_option.addLayout(layout_tab_custom_option_mid)
        layout_tab_custom_option.addLayout(layout_tab_custom_option_down)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(12)

        label_custom_select_num = QLabel('Profile ID        ')
        label_custom_select_num.setFont(font)

        self.label_custom_select_num = QLabel('00 / 32')
        self.label_custom_select_num.setFont(font)
        self.lineedit_custom_select_num = QLineEdit(16*'0' + '-' + 16*'0' + '-' + 16*'0')
        self.lineedit_custom_select_num.setFont(font)
        self.data_lineedit_custom_select_num = self.lineedit_custom_select_num.text()

        self.pushbutton_custom_select_num = QPushButton('&Ok')

        layout_tab_custom_option_up.addWidget(label_custom_select_num)
        layout_tab_custom_option_up.addWidget(self.lineedit_custom_select_num)
        layout_tab_custom_option_up.addWidget(self.pushbutton_custom_select_num)
        layout_tab_custom_option_down.addStretch(1)
        layout_tab_custom_option_down.setAlignment(Qt.AlignBottom)
        layout_tab_custom_option_down.addWidget(self.label_custom_select_num)

        groupbox_custom_option_channel_a = QGroupBox('A')
        groupbox_custom_option_channel_a.setAlignment(Qt.AlignCenter)
        groupbox_custom_option_channel_a.setStyleSheet("""
                                                     QGroupBox{
                                                     font-family: MonoxRegular;
                                                     font-size: 20px;
                                                     }
                                                     """)
        groupbox_custom_option_channel_b = QGroupBox('B')
        groupbox_custom_option_channel_b.setAlignment(Qt.AlignCenter)
        groupbox_custom_option_channel_b.setStyleSheet("""
                                                     QGroupBox{
                                                     font-family: MonoxRegular;
                                                     font-size: 20px;
                                                     }
                                                     """)
        groupbox_custom_option_channel_c = QGroupBox('C')
        groupbox_custom_option_channel_c.setAlignment(Qt.AlignCenter)
        groupbox_custom_option_channel_c.setStyleSheet("""
                                                     QGroupBox{
                                                     font-family: MonoxRegular;
                                                     font-size: 20px;
                                                     }
                                                     """)
        self.list_checkbox_channel = []
        for i in range(192):
            checkbox_select = QCheckBox('%03i' % (i + 1))
            checkbox_select.setStyleSheet("""
                                          QCheckBox{
                                          font-family: MonoxRegular;
                                          font-size: 15px;
                                          }
                                          """)
            self.list_checkbox_channel.append(checkbox_select)

        layout_tab_custom_option_mid.addWidget(groupbox_custom_option_channel_a)
        layout_tab_custom_option_mid.addWidget(groupbox_custom_option_channel_b)
        layout_tab_custom_option_mid.addWidget(groupbox_custom_option_channel_c)

        list_layout_custom_option_channel_global = []
        for i in range(3):
            list_layout_custom_option_channel_global.append(QHBoxLayout())

        groupbox_custom_option_channel_a.setLayout(list_layout_custom_option_channel_global[0])
        groupbox_custom_option_channel_b.setLayout(list_layout_custom_option_channel_global[1])
        groupbox_custom_option_channel_c.setLayout(list_layout_custom_option_channel_global[2])

        list_layout_custom_option_channel = []

        num = 12
        for i in range(num):
            list_layout_custom_option_channel.append(QVBoxLayout())
            list_layout_custom_option_channel[i].setAlignment(Qt.AlignCenter)

        for i in range(3):
            for j in range(num // 3):
                list_layout_custom_option_channel_global[i].addLayout(list_layout_custom_option_channel[(num // 3)*i + j])

        for i in range(num):
            for j in range(192 // num):
                list_layout_custom_option_channel[i].addWidget(self.list_checkbox_channel[(192 // num)*i + j])

        layout_graph_control = QVBoxLayout()
        layout_graph_control.setAlignment(Qt.AlignBottom)
        #layout_graph_control.setSpacing()
        self.graph_control.setLayout(layout_graph_control)

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
        layout_graph_control.addWidget(self.lcdnumber_countdown)

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
        layout_graph_control.addWidget(self.lcdnumber_countdown_num)

        self.pushbutton_graph_save = QPushButton('Save')
        self.pushbutton_graph_save.setStyleSheet("""
                                                 QPushButton{
                                                 min-width: 150px;
                                                 min-height: 60px;
                                                 }
                                                 """)
        widget_control_button = QWidget()
        widget_control_button.setStyleSheet("""
                                            QWidget{
                                            min-height: 300px;
                                            }
                                            """)
        layout_graph_control_button = QVBoxLayout()
        widget_control_button.setLayout(layout_graph_control_button)
        layout_graph_control_button.setAlignment(Qt.AlignBottom)
        layout_graph_control_button.addWidget(self.pushbutton_graph_save)
        layout_graph_control.addWidget(widget_control_button)

    def closeEvent(self, e):
        self.judge_close = True
        super(WindowGraphShow, self).closeEvent(e)

    def isClosed(self):
        return self.judge_close



if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowGraphShow()
    win.show()
    sys.exit(app.exec_())

