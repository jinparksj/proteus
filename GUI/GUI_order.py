__author__ = "Sungjin Park (jinparksj@gmail.com)"


from PyQt5.QtWidgets import QWidget, QTreeWidget, QSpinBox, QTreeWidgetItem, QPushButton, QBoxLayout, QLabel
from PyQt5.QtCore import Qt

from GUI import GUI_source_target
import Visual_top_side

SOURCE_TARGET_AMOUNT_DICT = {}


class OrderUI(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("Order Processing")
        self.box = QBoxLayout(QBoxLayout.TopToBottom)
        self.setFixedWidth(600)
        self.setFixedHeight(600)


        self.pb_previous = QPushButton("Previous")
        self.pb_next = QPushButton("Next")

        self.instruction = QLabel("Choose target, resource, and amount")
        self.tw = QTreeWidget(self)
        self.box.addWidget(self.instruction)
        self.box.addWidget(self.tw)
        self.tw.setColumnCount(2)
        self.tw.setHeaderLabels(["Sources", "Targets"])
        for source in GUI_source_target.SOURCELIST:
            root = QTreeWidgetItem(self.tw)
            root.setText(0, source)
            root.setText(1, source + 'Amount')
            for target in GUI_source_target.TARGETLIST:
                item = QTreeWidgetItem()
                item.setText(0, target)
                root.addChild(item)
                spbx = QSpinBox()
                spbx.setMaximum(1)
                self.tw.setItemWidget(item, 1, spbx)
        pb_layout = QBoxLayout(QBoxLayout.LeftToRight)
        pb_layout.addWidget(self.pb_previous)
        pb_layout.addWidget(self.pb_next)
        self.box.addLayout(pb_layout)

        self.setLayout(self.box)

class OrderProcess(OrderUI):
    def __init__(self):
        OrderUI.__init__(self)
        # super(OrderProcess, self).__init__()
        self.windows = list()

        self.pb_previous.clicked.connect(self.previousGUI)
        self.pb_next.clicked.connect(self.simulation)

    def previousGUI(self):
        window = GUI_source_target.SourceTarget()
        self.windows.append(window)
        self.close()
        window.show()

    def simulation(self):

        self.close()
        Visual_top_side.main()









