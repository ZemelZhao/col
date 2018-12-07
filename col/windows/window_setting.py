#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QSize, QRect, QDate, QTime
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QStackedWidget, QHBoxLayout,
                             QListWidgetItem, QLabel, QPushButton, QTabWidget,
                             QLineEdit, QRadioButton, QTextEdit, QVBoxLayout,
                             QGroupBox, QComboBox, QCheckBox, QSpinBox,
                             QTimeEdit, QDateEdit, QFrame)
import time

__Author__ = 'Zhao Zeming'
__Version__ = 1.0

class WindowOption(QWidget):
    def __init__(self):
        super(WindowOption, self).__init__()
        self.initUI()

    def initUI(self):
        """# Global """
        self.setWindowTitle('Option')
        self.setFixedSize(800, 450)

        self.list_option = QListWidget(self)
        self.stack_window = QStackedWidget(self)

        layout_main = QHBoxLayout(spacing=0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        layout_main.addWidget(self.list_option)
        layout_main.addWidget(self.stack_window)
        self.setLayout(layout_main)

        self.list_option.setStyleSheet("""
                                       QListWidget{
                                       min-width: 120px;
                                       max-width: 120px;
                                       color: white;
                                       background: grey;
                                       }
                                       """)


        """# List Option"""
        self.list_option.setFrameShape(QListWidget.NoFrame)
        self.list_option.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_option.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.list_option.currentRowChanged.connect(self.stack_window.setCurrentIndex)

        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(20)

        item = QListWidgetItem()
        item.setFont(font)
        item.setText('Lite')
        item.setSizeHint(QSize(0, 60))
        item.setTextAlignment(Qt.AlignCenter)
        self.list_option.addItem(item)

        item = QListWidgetItem()
        item.setFont(font)
        item.setText('Pro')
        item.setSizeHint(QSize(0, 60))
        item.setTextAlignment(Qt.AlignCenter)
        self.list_option.addItem(item)


        """# Stack Window"""
        """# Page 0"""
        self.page0 = QWidget()

        self.tabwidget_page0 = QTabWidget(self.page0)

        self.tab0_page0 = QWidget(self.page0)
        self.tab1_page0 = QWidget(self.page0)

        self.tabwidget_page0.addTab(self.tab0_page0, 'Info')
        self.tabwidget_page0.addTab(self.tab1_page0, 'Option')

        """# Page0 Tab0"""
        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(12)

        label_date_page0 = QLabel('Date      ')
        label_date_page0.setFont(font)

        label_time_page0 = QLabel('Time      ')
        label_time_page0.setFont(font)

        label_loc_page0 = QLabel('Location  ')
        label_loc_page0.setFont(font)

        label_users_name_page0 = QLabel('Name     ')
        label_users_name_page0.setFont(font)

        font_spe = QFont()
        font_spe.setFamily('MonoxRegular Bold')
        font_spe.setPointSize(12)
        label_users_gender_page0 = QLabel('Gender')
        label_users_gender_page0.setFont(font_spe)

        label_note_page0 = QLabel('Note')
        label_note_page0.setFont(font)

        self.dateedit_date_page0 = QDateEdit(QDate.currentDate())
        self.dateedit_date_page0.setDisplayFormat('yyyy/MM/dd')
        self.dateedit_date_page0.setCalendarPopup(True)
        self.dateedit_date_page0.setFont(font)
        self.timeedit_time_page0 = QTimeEdit(QTime.currentTime())
        self.timeedit_time_page0.setDisplayFormat('HH : mm')
        self.timeedit_time_page0.setFont(font)
        self.lineedit_loc_page0 = QLineEdit('Mars')
        self.lineedit_loc_page0.setFont(font)
        self.lineedit_users_name_page0 = QLineEdit('Object')
        self.lineedit_users_name_page0.setFont(font)

        self.radiobutton_users_gender_male_page0 = QRadioButton('Male')
        self.radiobutton_users_gender_female_page0 = QRadioButton('Female')
        self.radiobutton_users_gender_secret_page0 = QRadioButton('Secret')

        self.textedit_note_page0 = QTextEdit('None')
        self.textedit_note_page0.setFont(font)

        line_split_page0 = QFrame()
        line_split_page0.setFrameShape(QFrame.VLine)
        line_split_page0.setFrameShadow(QFrame.Sunken)

        groupbox_radio_button = QGroupBox()
        groupbox_radio_button.setStyleSheet("""
                                            QGroupBox{
                                            border: None;
                                            }
                                            """)

        layout_groupbox_radio_button = QHBoxLayout()
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_male_page0)
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_female_page0)
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_secret_page0)
        groupbox_radio_button.setLayout(layout_groupbox_radio_button)

        layout_tab0_page0_global = QVBoxLayout(self.tab0_page0)

        layout_info_page0 = QHBoxLayout()
        layout_note_page0 = QVBoxLayout()

        layout_time_page0 = QVBoxLayout()
        layout_user_page0 = QVBoxLayout()

        layout_date_page0 = QHBoxLayout()
        layout_date_page0.setAlignment(Qt.AlignLeft)
        layout_clock_page0 = QHBoxLayout()
        layout_clock_page0.setAlignment(Qt.AlignLeft)
        layout_loc_page0 = QHBoxLayout()
        layout_loc_page0.setAlignment(Qt.AlignLeft)
        layout_name_page0 = QHBoxLayout()
        layout_gender_page0 = QVBoxLayout()

        layout_date_page0.addWidget(label_date_page0)
        layout_date_page0.addWidget(self.dateedit_date_page0)
        layout_clock_page0.addWidget(label_time_page0)
        layout_clock_page0.addWidget(self.timeedit_time_page0)
        layout_loc_page0.addWidget(label_loc_page0)
        layout_loc_page0.addWidget(self.lineedit_loc_page0)
        layout_name_page0.addWidget(label_users_name_page0)
        layout_name_page0.addWidget(self.lineedit_users_name_page0)
        layout_gender_page0.addWidget(label_users_gender_page0)
        layout_gender_page0.addWidget(groupbox_radio_button)

        layout_time_page0.addLayout(layout_date_page0)
        layout_time_page0.addLayout(layout_clock_page0)
        layout_time_page0.addLayout(layout_loc_page0)
        layout_user_page0.addLayout(layout_name_page0)
        layout_user_page0.addLayout(layout_gender_page0)

        layout_info_page0.addLayout(layout_time_page0)
        layout_info_page0.addWidget(line_split_page0)
        layout_info_page0.addLayout(layout_user_page0)

        layout_note_page0.addWidget(label_note_page0)
        layout_note_page0.addWidget(self.textedit_note_page0)

        layout_tab0_page0_global.addLayout(layout_info_page0)
        layout_tab0_page0_global.addLayout(layout_note_page0)

        self.tab0_page0.setLayout(layout_tab0_page0_global)

        """# Page0 Tab1"""



        """# Page0 Global"""
        self.pushbutton_ok_page0 = QPushButton('&Ok')
        self.pushbutton_re_page0 = QPushButton('&Reset')
        self.pushbutton_de_page0 = QPushButton('&Cancel')

        layout_page0_option = QHBoxLayout()
        layout_page0_option.addStretch(1)
        layout_page0_option.addWidget(self.pushbutton_ok_page0)
        layout_page0_option.addWidget(self.pushbutton_re_page0)
        layout_page0_option.addWidget(self.pushbutton_de_page0)


        layout_page0_global = QVBoxLayout(self.page0)
        layout_page0_global.addWidget(self.tabwidget_page0)
        layout_page0_global.addLayout(layout_page0_option)

        self.stack_window.addWidget(self.page0)

        """# Page 1"""
        self.page1 = QWidget()

        self.tabwidget_page1 = QTabWidget(self.page1)

        self.tab0_page1 = QWidget(self.page1)
        self.tab1_page1 = QWidget(self.page1)

        self.tabwidget_page1.addTab(self.tab0_page1, 'Info')
        self.tabwidget_page1.addTab(self.tab1_page1, 'Option')

        """# Page1 Tab0"""
        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(12)

        label_date_page1 = QLabel('Date      ')
        label_date_page1.setFont(font)

        label_time_page1 = QLabel('Time      ')
        label_time_page1.setFont(font)

        label_loc_page1 = QLabel('Location  ')
        label_loc_page1.setFont(font)

        label_users_name_page1 = QLabel('Name     ')
        label_users_name_page1.setFont(font)

        label_users_gender_page1 = QLabel('Gender')
        label_users_gender_page1.setFont(font)

        label_note_page1 = QLabel('Note')
        label_note_page1.setFont(font)

        line_split_page1 = QFrame()
        line_split_page1.setFrameShape(QFrame.VLine)
        line_split_page1.setFrameShadow(QFrame.Sunken)

        self.dateedit_date_page1 = QDateEdit(QDate.currentDate())
        self.dateedit_date_page1.setDisplayFormat('yyyy/MM/dd')
        self.dateedit_date_page1.setCalendarPopup(True)
        self.dateedit_date_page1.setFont(font)
        self.timeedit_time_page1 = QTimeEdit(QTime.currentTime())
        self.timeedit_time_page1.setDisplayFormat('HH : mm')
        self.timeedit_time_page1.setFont(font)
        self.lineedit_loc_page1 = QLineEdit('Mars')
        self.lineedit_loc_page1.setFont(font)
        self.lineedit_users_name_page1 = QLineEdit('Object')
        self.lineedit_users_name_page1.setFont(font)

        self.radiobutton_users_gender_male_page1 = QRadioButton('Male')
        self.radiobutton_users_gender_female_page1 = QRadioButton('Female')
        self.radiobutton_users_gender_secret_page1 = QRadioButton('Secret')

        self.textedit_note_page1 = QTextEdit('None')
        self.textedit_note_page1.setFont(font)

        groupbox_radio_button = QGroupBox()
        groupbox_radio_button.setStyleSheet("""
                                            QGroupBox{
                                            border: None;
                                            }
                                            """)

        layout_groupbox_radio_button = QHBoxLayout()
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_male_page1)
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_female_page1)
        layout_groupbox_radio_button.addWidget(self.radiobutton_users_gender_secret_page1)
        groupbox_radio_button.setLayout(layout_groupbox_radio_button)

        layout_tab0_page1_global = QVBoxLayout(self.tab0_page1)

        layout_info_page1 = QHBoxLayout()
        layout_note_page1 = QVBoxLayout()

        layout_time_page1 = QVBoxLayout()
        layout_user_page1 = QVBoxLayout()

        layout_date_page1 = QHBoxLayout()
        layout_date_page1.setAlignment(Qt.AlignLeft)
        layout_clock_page1 = QHBoxLayout()
        layout_clock_page1.setAlignment(Qt.AlignLeft)
        layout_loc_page1 = QHBoxLayout()
        layout_loc_page1.setAlignment(Qt.AlignLeft)
        layout_name_page1 = QHBoxLayout()
        layout_gender_page1 = QVBoxLayout()

        layout_date_page1.addWidget(label_date_page1)
        layout_date_page1.addWidget(self.dateedit_date_page1)
        layout_clock_page1.addWidget(label_time_page1)
        layout_clock_page1.addWidget(self.timeedit_time_page1)
        layout_loc_page1.addWidget(label_loc_page1)
        layout_loc_page1.addWidget(self.lineedit_loc_page1)
        layout_name_page1.addWidget(label_users_name_page1)
        layout_name_page1.addWidget(self.lineedit_users_name_page1)
        layout_gender_page1.addWidget(label_users_gender_page1)
        layout_gender_page1.addWidget(groupbox_radio_button)

        layout_time_page1.addLayout(layout_date_page1)
        layout_time_page1.addLayout(layout_clock_page1)
        layout_time_page1.addLayout(layout_loc_page1)
        layout_user_page1.addLayout(layout_name_page1)
        layout_user_page1.addLayout(layout_gender_page1)

        layout_info_page1.addLayout(layout_time_page1)
        layout_info_page1.addWidget(line_split_page1)
        layout_info_page1.addLayout(layout_user_page1)

        layout_note_page1.addWidget(label_note_page1)
        layout_note_page1.addWidget(self.textedit_note_page1)

        layout_tab0_page1_global.addLayout(layout_info_page1)
        layout_tab0_page1_global.addLayout(layout_note_page1)

        self.tab0_page1.setLayout(layout_tab0_page1_global)

        """# Page1 Tab1"""
        font = QFont()
        font.setFamily('MonoxLight')
        font.setPointSize(12)

        label_filter_or_not = QLabel('Filter')
        label_filter_or_not.setFont(font)

        label_filter_hz1 = QLabel('Hz')
        label_filter_hz1.setFont(font)
        label_filter_hz2 = QLabel('Hz')
        label_filter_hz2.setFont(font)
        label_filter_hz3 = QLabel('Hz')
        label_filter_hz3.setFont(font)
        label_filter_hz4 = QLabel('Hz')
        label_filter_hz4.setFont(font)

        label_sampling_freq = QLabel('Sampling Frequency')
        label_sampling_freq.setFont(font)

        label_notch_filter = QLabel('Notch Filter')
        label_notch_filter.setFont(font)

        label_bandpass_filter = QLabel('Bandpass Filter')
        label_bandpass_filter.setFont(font)

        label_bandpass_filter_to = QLabel('to')
        label_bandpass_filter_to.setFont(font)

        label_set_num = QLabel('Set Number')
        label_set_num.setFont(font)

        label_set_time = QLabel('Set Time')
        label_set_time.setFont(font)

        label_set_interval = QLabel('Auto Restart')
        label_set_interval.setFont(font)

        label_set_interval_s = QLabel('s')
        label_set_interval_s.setFont(font)

        label_tcp_address = QLabel('TCP Address')
        label_tcp_address.setFont(font)

        label_tcp_port = QLabel('TCP Port')
        label_tcp_port.setFont(font)

        label_filetype_save = QLabel('Filetype')
        label_filetype_save.setFont(font)

        label_channel_num = QLabel('Channel Number')
        label_channel_num.setFont(font)

        self.spinbox_set_num = QSpinBox()
        self.spinbox_set_time = QSpinBox()

        self.lineedit_tcp_address = QLineEdit()
        self.lineedit_tcp_address.setFont(font)

        self.lineedit_tcp_port = QLineEdit()
        self.lineedit_tcp_port.setFont(font)

        self.combobox_bandpass_high = QComboBox()
        self.combobox_bandpass_high.addItem('1')
        self.combobox_bandpass_high.addItem('5')
        self.combobox_bandpass_high.addItem('10')
        self.combobox_bandpass_high.addItem('20')

        self.combobox_bandpass_low = QComboBox()
        self.combobox_bandpass_low.addItem('50')
        self.combobox_bandpass_low.addItem('100')
        self.combobox_bandpass_low.addItem('200')
        self.combobox_bandpass_low.addItem('450')

        self.combobox_sampling_freq = QComboBox()
        self.combobox_sampling_freq.addItem('250')
        self.combobox_sampling_freq.addItem('500')
        self.combobox_sampling_freq.addItem('1000')
        self.combobox_sampling_freq.addItem('2000')

        self.combobox_notch_filter = QComboBox()
        self.combobox_notch_filter.addItem('50')
        self.combobox_notch_filter.addItem('60')

        self.combobox_filetype_save = QComboBox()
        self.combobox_filetype_save.addItem('csv')
        self.combobox_filetype_save.addItem('npy')

        self.combobox_channel_num = QComboBox()
        self.combobox_channel_num.addItem('64')
        self.combobox_channel_num.addItem('128')
        self.combobox_channel_num.addItem('192')

        self.checkbox_notch_filter = QCheckBox('Notch Filter')
        self.checkbox_bandpass_filter = QCheckBox('Bandpass Filter')

        self.radiobutton_restart_auto = QRadioButton('Auto Restart')
        self.radiobutton_restart_press = QRadioButton('Manual Restart')

        self.spinbox_restart_auto = QSpinBox()

        self.pushbutton_reset_filter = QPushButton('Reset')
        self.pushbutton_reset_data = QPushButton('Reset')
        self.pushbutton_reset_tcpip = QPushButton('Reset')

        groupbox_filter_page1 = QGroupBox('Filter')
        groupbox_filter_page1.setStyleSheet("""
                                            QGroupBox{
                                            font-family: MonoxRegular;
                                            font-size: 20px;
                                            }
                                            """)
        groupbox_data_page1 = QGroupBox('Data')
        groupbox_data_page1.setStyleSheet("""
                                            QGroupBox{
                                            font-family: MonoxRegular;
                                            font-size: 20px;
                                            }
                                        """)
        groupbox_tcpip_page1 = QGroupBox('TCP/IP')
        groupbox_tcpip_page1.setStyleSheet("""
                                            QGroupBox{
                                            font-family: MonoxRegular;
                                            font-size: 20px;
                                            }
                                        """)


        layout_filter_or_not = QHBoxLayout()
        layout_filter_notch = QHBoxLayout()
        layout_filter_bandpass = QHBoxLayout()
        layout_sampling_freq = QHBoxLayout()
        layout_button_filter_reset = QHBoxLayout()

        layout_filter_or_not.addWidget(label_filter_or_not)
        layout_filter_or_not.addWidget(self.checkbox_notch_filter)
        layout_filter_or_not.addWidget(self.checkbox_bandpass_filter)

        layout_filter_notch.addWidget(label_notch_filter)
        layout_filter_notch.addWidget(self.combobox_notch_filter)
        layout_filter_notch.addWidget(label_filter_hz1)

        layout_filter_bandpass.addWidget(label_bandpass_filter)
        layout_filter_bandpass.addWidget(self.combobox_bandpass_high)
        layout_filter_bandpass.addWidget(label_filter_hz2)
        layout_filter_bandpass.addWidget(label_bandpass_filter_to)
        layout_filter_bandpass.addWidget(self.combobox_bandpass_low)
        layout_filter_bandpass.addWidget(label_filter_hz3)

        layout_sampling_freq.addWidget(label_sampling_freq)
        layout_sampling_freq.addWidget(self.combobox_sampling_freq)
        layout_sampling_freq.addWidget(label_filter_hz4)

        layout_button_filter_reset.addWidget(self.pushbutton_reset_filter)

        layout_data_channel_num = QHBoxLayout()
        layout_data_set = QHBoxLayout()
        layout_data_interval = QVBoxLayout()
        layout_data_filetype = QHBoxLayout()
        layout_button_data_reset = QHBoxLayout()

        layout_data_channel_num.addWidget(label_channel_num)
        layout_data_channel_num.addWidget(self.combobox_channel_num)
        layout_data_interval_auto = QHBoxLayout()
        layout_data_interval_press = QHBoxLayout()
        layout_data_interval_auto.addWidget(self.radiobutton_restart_auto)
        layout_data_interval_auto.addWidget(self.spinbox_restart_auto)
        layout_data_interval_auto.addWidget(label_set_interval_s)
        layout_data_interval_press.addWidget(self.radiobutton_restart_press)

        layout_data_interval.addLayout(layout_data_interval_auto)
        layout_data_interval.addLayout(layout_data_interval_press)

        layout_data_set.addWidget(label_set_num)
        layout_data_set.addWidget(self.spinbox_set_num)
        layout_data_set.addWidget(label_set_time)
        layout_data_set.addWidget(self.spinbox_set_time)

        layout_data_filetype.addWidget(label_filetype_save)
        layout_data_filetype.addWidget(self.combobox_filetype_save)

        layout_button_data_reset.addWidget(self.pushbutton_reset_data)

        layout_filter_page1 = QVBoxLayout()
        layout_filter_page1.addLayout(layout_filter_or_not)
        layout_filter_page1.addLayout(layout_filter_notch)
        layout_filter_page1.addLayout(layout_filter_bandpass)
        layout_filter_page1.addLayout(layout_sampling_freq)
        layout_filter_page1.addLayout(layout_button_filter_reset)

        layout_data_page1 = QVBoxLayout()
        layout_data_page1.addLayout(layout_data_channel_num)
        layout_data_page1.addLayout(layout_data_set)
        layout_data_page1.addLayout(layout_data_interval)
        layout_data_page1.addLayout(layout_data_filetype)
        layout_data_page1.addLayout(layout_button_data_reset)

        layout_tcpip_page1_global = QVBoxLayout()
        layout_tcpip_data = QHBoxLayout()
        layout_tcpip_button_reset = QHBoxLayout()

        layout_tcpip_data.addWidget(label_tcp_address)
        layout_tcpip_data.addWidget(self.lineedit_tcp_address)
        layout_tcpip_data.addWidget(label_tcp_port)
        layout_tcpip_data.addWidget(self.lineedit_tcp_port)

        layout_tcpip_button_reset.addWidget(self.pushbutton_reset_tcpip)

        layout_tcpip_page1_global.addLayout(layout_tcpip_data)
        layout_tcpip_page1_global.addLayout(layout_tcpip_button_reset)

        groupbox_filter_page1.setLayout(layout_filter_page1)
        groupbox_data_page1.setLayout(layout_data_page1)
        groupbox_tcpip_page1.setLayout(layout_tcpip_page1_global)

        layout_tab1_page1_up = QHBoxLayout()
        layout_tab1_page1_down = QHBoxLayout()

        layout_tab1_page1_up.addWidget(groupbox_filter_page1)
        layout_tab1_page1_up.addWidget(groupbox_data_page1)
        layout_tab1_page1_down.addWidget(groupbox_tcpip_page1)

        layout_tab1_page1_global = QVBoxLayout()
        layout_tab1_page1_global.addLayout(layout_tab1_page1_up)
        layout_tab1_page1_global.addLayout(layout_tab1_page1_down)

        self.tab1_page1.setLayout(layout_tab1_page1_global)


        """# Page1 Global"""
        self.pushbutton_ok_page1 = QPushButton('&Ok')
        self.pushbutton_de_page1 = QPushButton('&Cancel')
        self.pushbutton_re_page1 = QPushButton('&Reset')

        layout_page1_option = QHBoxLayout()
        layout_page1_option.addStretch(1)
        layout_page1_option.addWidget(self.pushbutton_ok_page1)
        layout_page1_option.addWidget(self.pushbutton_re_page1)
        layout_page1_option.addWidget(self.pushbutton_de_page1)

        layout_page1_global = QVBoxLayout()
        layout_page1_global.addWidget(self.tabwidget_page1)
        layout_page1_global.addLayout(layout_page1_option)

        self.page1.setLayout(layout_page1_global)

        self.stack_window.addWidget(self.page1)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = WindowOption()
    win.show()
    sys.exit(app.exec_())
