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

from PyQt5.QtCore import Qt

class SmallBed(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Small"))
        for i in range(12):
            for j in range(8):
                setattr(self, 'small_chkb_{}_{}'.format(i, j), QCheckBox())
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        grid_box = QGridLayout()
        for i in range(12):
            for j in range(8):
                temp_chkb = getattr(self, 'small_chkb_{}_{}'.format(i, j))
                grid_box.addWidget(temp_chkb, i, j)

        self.gb.setLayout(grid_box)
        layout.addWidget(self.gb)
        self.setLayout(layout)

class LargeBed(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Large"))
        for i in range(8):
            for j in range(8):
                setattr(self, 'large_chkb_{}_{}'.format(i, j), QCheckBox())
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        grid_box = QGridLayout()
        for i in range(8):
            for j in range(8):
                temp_chkb = getattr(self, 'large_chkb_{}_{}'.format(i, j))
                grid_box.addWidget(temp_chkb, i, j)

        self.gb.setLayout(grid_box)
        layout.addWidget(self.gb)
        self.setLayout(layout)

class MiddleBed(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Middle"))
        for i in range(10):
            for j in range(8):
                setattr(self, 'mid_chkb_{}_{}'.format(i, j), QCheckBox())
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        grid_box = QGridLayout()
        for i in range(10):
            for j in range(8):
                temp_chkb = getattr(self, 'mid_chkb_{}_{}'.format(i, j))
                grid_box.addWidget(temp_chkb, i, j)

        self.gb.setLayout(grid_box)
        layout.addWidget(self.gb)
        self.setLayout(layout)