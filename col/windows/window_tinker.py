#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QColor, QFont, QImage, QPixmap
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox,
                             QGridLayout, QLCDNumber, )
import os
import pyqtgraph as pg
import time

class WindowAbout(QWidget):
    def __init__(self):
        super(WindowAbout, self).__init__()
        myFolder = os.path.split(os.path.realpath(__file__))[0]
        self.loc_logo = os.path.join(myFolder, os.path.pardir, 'resource', 'logo.png')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('About')
        self.setFixedSize(400, 220)

        layout_global = QHBoxLayout()
        self.setLayout(layout_global)

        layout_logo = QVBoxLayout()
        layout_logo.setAlignment(Qt.AlignTop)
        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignTop)
        layout_global.addLayout(layout_logo)
        layout_global.addLayout(layout_main)

        label_logo = QLabel()
        img_width = 100
        img_height = 100
        img = QImage(self.loc_logo)
        pix_img = QPixmap.fromImage(img.scaled(QSize(img_width, img_height)))
        label_logo.resize(img_width, img_height)
        label_logo.setPixmap(pix_img)
        layout_logo.addWidget(label_logo)

        font = QFont()
        font.setFamily('MonoxRegular Bold')
        font.setPointSize(30)
        label_main_name = QLabel('COL')
        label_main_name.setFont(font)
        layout_main.addWidget(label_main_name)

        font = QFont()
        font.setFamily('MonoxRegular Bold')
        font.setPointSize(15)
        label_version_name = QLabel('Version 1.0.1')
        label_version_name.setFont(font)
        layout_main.addWidget(label_version_name)

        font = QFont()
        font.setFamily('Ubuntu Mono')
        font.setPointSize(12)
        label_dependency_name = QLabel('Using PyQt5')
        label_dependency_name.setFont(font)
        layout_main.addWidget(label_dependency_name)

        label_copyright_name = QLabel('CopyRight @2018-2020 Zhao Zeming')
        label_copyright_name.setFont(font)
        layout_main.addWidget(label_copyright_name)

        label_license_name = QLabel('License: ')
        label_license_name.setFont(font)
        layout_main.addWidget(label_license_name)

        label_github_name = QLabel('Project Hosted at Github')
        label_github_name.setFont(font)
        layout_main.addWidget(label_github_name)

        layout_button_ok = QHBoxLayout()
        layout_button_ok.setAlignment(Qt.AlignRight)
        layout_main.addLayout(layout_button_ok)
        self.pushbutton_ok = QPushButton('&Ok')
        layout_button_ok.addWidget(self.pushbutton_ok)

class WindowHelp(QWidget):
    def __init__(self):
        super(WindowHelp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Help')
        self.setFixedSize(250, 100)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(18)

        label_email = QLabel('Please e-mail to me: ')
        label_email.setFont(font)

        label_email_address = QLabel('zemzhao@163.com')
        label_email_address.setFont(font)

        self.pushbutton_ok = QPushButton('&OK')

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignCenter)
        self.setLayout(layout_main)
        layout_main.addWidget(label_email)
        layout_main.addWidget(label_email_address)

        layout_pushbutton_ok = QHBoxLayout()
        layout_pushbutton_ok.addStretch(1)
        layout_pushbutton_ok.addWidget(self.pushbutton_ok)

        layout_main.addLayout(layout_pushbutton_ok)




if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowHelp()
    win.show()
    sys.exit(app.exec_())

