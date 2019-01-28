__author__ = "Sungjin Park (jinparksj@gmail.com)"

import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton


from PyQt5.QtCore import Qt



from GUI.TestBed import SmallBed, LargeBed, MiddleBed
from GUI.SensorChip import SensorChipAssay
from GUI.GUI_source_target import SourceTarget

CHECKEDLIST = []

class Bed(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.gb = QGroupBox(self.tr("Bed"))
        self.small = SmallBed()
        self.large = LargeBed()
        self.mid = MiddleBed()
        self.init_widget()

    def init_widget(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, parent=self)
        self.setLayout(layout)

        # grid_box = QGridLayout()

        layout.addWidget(self.small)
        layout.addWidget(self.large)
        layout.addWidget(self.mid)

        self.gb.setLayout(layout)
        layout.addWidget(self.gb)
        self.setLayout(layout)

class Controller(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.pb_next = QPushButton("Next")
        self.pb_uncheck_all = QPushButton("Uncheck All")
        self.bed = Bed()
        self.sensor = SensorChipAssay()
        self.instruction1 = QLabel("Check vials or sensors using for test")
        self.instruction2 = QLabel("1. Uncheck All: Make all checkboxes unchecked")
        self.instruction3 = QLabel("2. Next: Go next stage to decide sources or targets with checked samples")
        self.windows = list()
        self.init_widget()


    def init_widget(self):
        self.setWindowTitle("Proteus Control GUI")
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        bed_lbx = QBoxLayout(QBoxLayout.RightToLeft, parent = self)
        sensor_lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        button_lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.setLayout(form_lbx)

        form_lbx.addWidget(self.instruction1)
        form_lbx.addWidget(self.instruction2)
        form_lbx.addWidget(self.instruction3)

        form_lbx.addLayout(sensor_lbx)
        sensor_lbx.addWidget(self.sensor)
        form_lbx.addLayout(bed_lbx)
        bed_lbx.addWidget(self.bed)
        form_lbx.addLayout(button_lbx)
        button_lbx.addWidget(self.pb_uncheck_all)
        button_lbx.addWidget(self.pb_next)

        self.pb_uncheck_all.clicked.connect(self.pushButtonUncheck)
        self.pb_next.clicked.connect(self.pushButtonNext)

    def pushButtonUncheck(self):
        window = Controller()
        self.windows.append(window)
        self.close()
        window.show()

    def pushButtonNext(self):
        # small
        for i in range(12):
            for j in range(8):
                temp_chkb = getattr(self.bed.small, 'small_chkb_{}_{}'.format(i, j))
                if temp_chkb.isChecked():
                    temp_small_text = 'small_' + str(i) + '_' + str(j)
                    CHECKEDLIST.append(temp_small_text)

        # large
        for i in range(8):
            for j in range(8):
                temp_chkb = getattr(self.bed.large, 'large_chkb_{}_{}'.format(i, j))
                if temp_chkb.isChecked():
                    temp_large_text = 'large_' + str(i) + '_' + str(j)
                    CHECKEDLIST.append(temp_large_text)

        # middle
        for i in range(10):
            for j in range(8):
                temp_chkb = getattr(self.bed.mid, 'mid_chkb_{}_{}'.format(i, j))
                if temp_chkb.isChecked():
                    temp_mid_text = 'mid_' + str(i) + '_' + str(j)
                    CHECKEDLIST.append(temp_mid_text)

        # sensor
        for k in range(6):
            temp_sensorchip = getattr(self.sensor, 'sensorchip_{}'.format(k))
            for i in range(8):
                for j in range(2):
                    temp_chkb = getattr(temp_sensorchip, 'sensor_{}_{}'.format(i, j))
                    if temp_chkb.isChecked():
                        temp_sensor_text = 'sensor_' + str(k)+ '_' + str(i) + '_' + str(j)
                        CHECKEDLIST.append(temp_sensor_text)

        nextwindow = SourceTarget()
        self.windows.append(nextwindow)
        self.close()
        nextwindow.show()

def main():
    app = QApplication(sys.argv)
    ctrl = Controller()
    ctrl.show()
    exit(app.exec())

if __name__ == "__main__":
    main()