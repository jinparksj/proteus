__author__ = "Sungjin Park (jinparksj@gmail.com)"


from PyQt5.QtWidgets import QWidget, QTreeWidget, QSpinBox, QTreeWidgetItem, QPushButton, QBoxLayout, QLabel
from PyQt5.QtCore import Qt

from GUI import GUI_source_target
import Visual_top_side

SOURCE_TARGET_AMOUNT_DICT = {}
TARGET_AMOUNT_LIST = []

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
        self.tw = QTreeWidget()
        self.box.addWidget(self.instruction)
        self.box.addWidget(self.tw)
        self.tw.setColumnCount(2)
        self.tw.setColumnWidth(0, 250)
        self.tw.setHeaderLabels(["Sources", "Targets"])
        self.len_source = len(GUI_source_target.SOURCELIST)
        self.len_target = len(GUI_source_target.TARGETLIST)
        source_i = 0

        for source in GUI_source_target.SOURCELIST:
            target_j = 0
            root = QTreeWidgetItem(self.tw)
            root.setText(0, source)
            root.setText(1, source + '\'s Amount')
            for target in GUI_source_target.TARGETLIST:
                item = QTreeWidgetItem()
                item.setText(0, target)
                root.addChild(item)
                setattr(self, 'spbx_{}_{}'.format(source_i, target_j), QSpinBox())
                temp_spbx = getattr(self, 'spbx_{}_{}'.format(source_i, target_j))
                temp_spbx.setMaximum(5)
                self.tw.setItemWidget(item, 1, temp_spbx)
                target_j += 1
            source_i += 1


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
        GUI_source_target.TARGETLIST = []
        GUI_source_target.SOURCELIST = []
        window = GUI_source_target.SourceTarget()
        self.windows.append(window)
        self.close()
        window.show()

    def simulation(self):
        for i in range(self.len_source):
            TARGET_AMOUNT_LIST = []
            root = self.tw.topLevelItem(i)
            source = root.text(0)
            for j in range(self.len_target):
                item = root.child(j) #target
                target = item.text(0) #dict:key
                temp_target = getattr(self, 'spbx_{}_{}'.format(i, j))
                if temp_target.value() >= 1:
                    TARGET_AMOUNT_LIST.append([target, temp_target.value()])
            SOURCE_TARGET_AMOUNT_DICT.update({source: TARGET_AMOUNT_LIST})

        self.close()
        self.tw.close()
        Visual_top_side.main()









