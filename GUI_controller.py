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
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtSerialPort import QSerialPortInfo


from TestBed import SmallBed, LargeBed, MiddleBed
from SensorChip import SensorChipAssay

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
        self.pb_ok = QPushButton("Ok")
        self.pb_no = QPushButton("No")
        self.bed = Bed()
        self.sensor = SensorChipAssay()
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Proteus Control GUI")
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        bed_lbx = QBoxLayout(QBoxLayout.RightToLeft, parent = self)
        sensor_lbx = QBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.setLayout(form_lbx)

        form_lbx.addLayout(sensor_lbx)
        sensor_lbx.addWidget(self.sensor)
        form_lbx.addLayout(bed_lbx)
        bed_lbx.addWidget(self.bed)

        form_lbx.addWidget(self.pb_ok)
        form_lbx.addWidget(self.pb_no)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctrl = Controller()
    ctrl.show()
    exit(app.exec())