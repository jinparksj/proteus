__author__ = "Sungjin Park (jinparksj@gmail.com)"

import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QToolTip

from PyQt5.QtCore import Qt

class SensorChipAssay(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Bed"))
        for i in range(6):
            setattr(self, 'sensorchip_{}'.format(i), SensorChip())
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, parent=self)
        self.setLayout(layout)

        for i in range(6):
            temp_sensor = getattr(self, 'sensorchip_{}'.format(i))
            layout.addWidget(temp_sensor)

        self.gb.setLayout(layout)
        layout.addWidget(self.gb)
        self.setLayout(layout)



class SensorChip(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Sensor"))
        for i in range(8):
            for j in range(2):
                setattr(self, 'sensor_{}_{}'.format(i, j), QCheckBox())
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        grid_box = QGridLayout()
        for i in range(8):
            for j in range(2):
                temp_chkb = getattr(self, 'sensor_{}_{}'.format(i, j))
                grid_box.addWidget(temp_chkb, i, j)

        self.gb.setLayout(grid_box)
        layout.addWidget(self.gb)
        self.setLayout(layout)