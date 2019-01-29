__author__ = "Sungjin Park (jinparksj@gmail.com)"

from PyQt5.QtWidgets import QWidget, QTreeWidget, QPushButton, QTreeWidgetItem, QBoxLayout
from PyQt5.QtCore import Qt

from GUI import GUI_controller
from GUI import GUI_order

SOURCELIST = []
TARGETLIST = []


class ParentUI(QWidget):
    HEADER = ["Source", "Target"]

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("Select Source and Target")
        self.setFixedWidth(600)
        self.setFixedHeight(600)

        #TreeWidget Source
        self.source = QTreeWidget(self)
        self.source.setColumnCount(1)
        self.source.setHeaderLabels([self.HEADER[0]])

        #TreeWidgets Target
        self.target = QTreeWidget(self)
        self.target.setColumnCount(1)
        self.target.setHeaderLabels([self.HEADER[1]])

        #Buttons
        self.pb_move_left = QPushButton("<<<")
        self.pb_move_right = QPushButton(">>>")
        self.pb_previous = QPushButton("Previous")
        self.pb_next = QPushButton("Next")
        self.pb_up_source = QPushButton("∧")
        self.pb_down_source = QPushButton("∨")
        self.pb_up_target = QPushButton("∧")
        self.pb_down_target = QPushButton("∨")


        layout_up_down_source = QBoxLayout(QBoxLayout.TopToBottom)
        layout_up_down_source.addWidget(self.pb_up_source)
        layout_up_down_source.addWidget(self.pb_down_source)

        layout_up_down_target = QBoxLayout(QBoxLayout.TopToBottom)
        layout_up_down_target.addWidget(self.pb_up_target)
        layout_up_down_target.addWidget(self.pb_down_target)

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addLayout(layout_up_down_source)
        layout.addWidget(self.source)
        layout.addWidget(self.target)
        layout.addLayout(layout_up_down_target)

        button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        button_layout.addWidget(self.pb_previous)
        button_layout.addWidget(self.pb_move_right)
        button_layout.addWidget(self.pb_move_left)
        button_layout.addWidget(self.pb_next)

        main_layout = QBoxLayout(QBoxLayout.TopToBottom)
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


class SourceTarget(ParentUI):
    def __init__(self):
        ParentUI.__init__(self)
        #NEED TO GET DATA from GUI_Controller
        data = GUI_controller.CHECKEDLIST
        self.total_ind_len = len(data)
        parent = QTreeWidget.invisibleRootItem(self.source)
        for d in data:
            item = self.make_tree_item(d)
            parent.addChild(item)

        self.pb_move_right.clicked.connect(self.move_item)
        self.pb_move_left.clicked.connect(self.move_item)

        self.windows = list()
        self.pb_previous.clicked.connect(self.previousGUI)
        self.pb_up_source.clicked.connect(self.move_up_down)
        self.pb_down_source.clicked.connect(self.move_up_down)
        self.pb_up_target.clicked.connect(self.move_up_down)
        self.pb_down_target.clicked.connect(self.move_up_down)
        self.pb_next.clicked.connect(self.pushButtonNext)


    #NEED TO FIX
    def move_up_down(self):
        sender = self.sender()

        index_item = None
        item = None
        current = None
        auto_selected_item = None

        if self.pb_up_source == sender:
            current_tw = self.source
        elif self.pb_down_source == sender:
            current_tw = self.source
        elif self.pb_up_target == sender:
            current_tw = self.target
        elif self.pb_down_target == sender:
            current_tw = self.target

        item = current_tw.currentItem()

        if item.isSelected() and (self.pb_up_source == sender or self.pb_up_target == sender):
            current = QTreeWidget.invisibleRootItem(current_tw)
            index_item = current.indexOfChild(item)
            current.removeChild(item)
            # auto_selected_item = current.child((index_item - 1) % self.total_ind_len)
            current.insertChild((index_item - 1) % self.total_ind_len, item)
            selected_items = current_tw.selectedItems()
            for item in selected_items:
                item.setSelected(False)

        elif item.isSelected() and (self.pb_down_source == sender or self.pb_down_target == sender):
            current = QTreeWidget.invisibleRootItem(current_tw)
            index_item = current.indexOfChild(item)
            current.removeChild(item)
            # auto_selected_item = current.child((index_item - 1) % self.total_ind_len)
            current.insertChild((index_item + 1) % self.total_ind_len, item)
            selected_items = current_tw.selectedItems()
            for item in selected_items:
                item.setSelected(False)

        top_item_source = self.source.topLevelItem(0)
        top_item_target = self.target.topLevelItem(0)

        top_item_source.setSelected(True)
        top_item_target.setSelected(True)
        self.source.setCurrentItem(top_item_source)
        self.target.setCurrentItem(top_item_target)


    def TWtoList(self, tw, LIST):
        item = True
        while item != None:
            item = tw.takeTopLevelItem(tw.currentColumn())
            if item == None:
                break
            str_item = item.text(0)
            LIST.append(str_item)

    def pushButtonNext(self):

        self.TWtoList(self.source, SOURCELIST)
        self.TWtoList(self.target, TARGETLIST)


        nextwindow = GUI_order.OrderProcess()
        self.windows.append(nextwindow)
        self.close()
        nextwindow.show()

    def previousGUI(self):
        window = GUI_controller.Controller()
        self.windows.append(window)
        GUI_controller.CHECKEDLIST = []
        self.close()
        window.show()

    @classmethod
    def make_tree_item(cls, name:str):
        item = QTreeWidgetItem()
        item.setText(0, name)
        return item

    def move_item(self):
        sender = self.sender()
        if self.pb_move_right == sender:
            source_tw = self.source
            target_tw = self.target
        elif self.pb_move_left == sender:
            source_tw = self.target
            target_tw = self.source

        item_source = source_tw.currentItem()
        source = QTreeWidget.invisibleRootItem(source_tw)
        source.removeChild(item_source)

        target = QTreeWidget.invisibleRootItem(target_tw)
        target.addChild(item_source)

        item_source = source_tw.currentItem()
        if item_source != None:
            item_source.setSelected(False)

        top_item_source = source_tw.topLevelItem(0)
        top_item_target = target_tw.topLevelItem(0)
        if top_item_source != None:
            top_item_source.setSelected(True)
            source_tw.setCurrentItem(top_item_source)
        if top_item_target != None:
            top_item_target.setSelected(True)
            target_tw.setCurrentItem(top_item_target)


