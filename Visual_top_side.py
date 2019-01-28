__author__ = "Sungjin Park (jinparksj@gmail.com)"

import cv2
import numpy as np
import time
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt

from GUI import GUI_order
from GUI import GUI_controller


SOURCE_LIST = []
TARGET_LIST = []

SCALE = 1.5

WORKSPACE_HEIGHT = 500 * SCALE
WORKSPACE_WIDTH = 700 * SCALE

MARGIN = 80 * SCALE
MIDBEDSIZE_HEIGHT = 93 * SCALE * 2
MIDBEDSIZE_WIDTH = 75 * SCALE * 2
MIDVIAL_RADIUS = 3 * 2 * SCALE
MID_GAP = 3 * 2 * SCALE * 1.8
MID_VIAL_LIST = []
MID_VIAL_DICT = {}


LARGEBEDSIZE_HEIGHT = 93 * SCALE * 2
LARGEBEDSIZE_WIDTH = 91 * SCALE * 2
LARGEVIAL_RADIUS = 4.2 * 2 * SCALE
LARGE_GAP = 3.5 * 2 * SCALE * 1.8
LARGE_VIAL_LIST = []
LARGE_VIAL_DICT = {}

GAP_BED = 15 * SCALE

SMALLBEDSIZE_HEIGHT = 74 * SCALE * 2
SMALLBEDSIZE_WIDTH = 50 * SCALE * 2
SMALLVIAL_RADIUS = 2.2 * 2 * SCALE
SMALL_GAP = 2 * 2 * SCALE * 1.8
SMALL_VIAL_LIST = []
SMALL_VIAL_DICT = {}

SENSOR_HEIGHT = 45 * SCALE * 2
SENSOR_WIDTH = 15 * SCALE * 2
SENSOR_RADIUS = 1.5 * 2 * SCALE
SENSOR_GAP = 2 * 2 * SCALE * 1.8
SENSOR_VIAL_LIST = []
SENSOR_VIAL_DICT = {}
GAP_ASSAY = 50 * SCALE

A2 = 30 * SCALE

WORKPOINT_DICT = {}
WORKPROCESS_LIST = []

STEP = 5

class Workspace(object):
    def __init__(self):
        self.workspace = np.zeros((int(WORKSPACE_HEIGHT), int(WORKSPACE_WIDTH), 3), np.uint8)
        self.workspace[:] = 255
        self.height = self.workspace.shape[0] #row
        self.width = self.workspace.shape[1] #col
        # self.workspace = cv2.line(self.workspace, (100, 100), (500, 500), (255, 0, 0), 5)

        #MID BED
        mid_lefttop = (int(MARGIN), int(self.height - MARGIN - MIDBEDSIZE_HEIGHT))
        mid_rightbottom = (int(MARGIN + MIDBEDSIZE_WIDTH), int(self.height - MARGIN))

        self.workspace = cv2.rectangle(self.workspace, mid_lefttop, mid_rightbottom, (0, 0, 0), 2)

        #LARGE BED
        large_lefttop = (int(MARGIN + GAP_BED + MIDBEDSIZE_WIDTH), int(self.height - MARGIN - LARGEBEDSIZE_HEIGHT ))
        large_rightbottom = (int(MARGIN + MIDBEDSIZE_WIDTH + GAP_BED + LARGEBEDSIZE_WIDTH), int(self.height - MARGIN))
        self.workspace = cv2.rectangle(self.workspace, large_lefttop, large_rightbottom, (0, 0, 0), 2)

        #SMALL BED
        small_lefttop = (int(MARGIN + 2 * GAP_BED + MIDBEDSIZE_WIDTH + LARGEBEDSIZE_WIDTH),
                         int(self.height - MARGIN - SMALLBEDSIZE_HEIGHT))
        small_rightbottom = (int(MARGIN + MIDBEDSIZE_WIDTH + 2 * GAP_BED + LARGEBEDSIZE_WIDTH + SMALLBEDSIZE_WIDTH),
                             int(self.height - MARGIN))
        self.workspace = cv2.rectangle(self.workspace, small_lefttop, small_rightbottom, (0, 0, 0), 2)

        #Vials
        #1. Mid
        for i in range(1, 11): #i: row, y
            for j in range(1, 9): #j: col, x
                x = mid_lefttop[0] + int(MID_GAP + MIDVIAL_RADIUS) * j
                y = mid_lefttop[1] + int(MID_GAP + MIDVIAL_RADIUS) * i
                cv2.circle(self.workspace, (x, y), int(MIDVIAL_RADIUS), (0, 0, 0))
                MID_VIAL_LIST.append([y, x])
                MID_VIAL_DICT.update({'mid_{}_{}'.format(i-1, j-1) : [y, x]})

        #2. Large
        for i in range(1, 9): #i: row, y
            for j in range(1, 9): #j: col, x
                x = large_lefttop[0] + int(LARGE_GAP + LARGEVIAL_RADIUS) * j
                y = large_lefttop[1] + int(LARGE_GAP + LARGEVIAL_RADIUS) * i
                cv2.circle(self.workspace, (x, y), int(LARGEVIAL_RADIUS), (0, 0, 0))
                LARGE_VIAL_LIST.append([y, x])
                LARGE_VIAL_DICT.update({'large_{}_{}'.format(i-1, j-1): [y, x]})

        #3. Small
        for i in range(1, 13): #i: row, y
            for j in range(1, 9): #j: col, x
                x = small_lefttop[0] + int(SMALL_GAP + SMALLVIAL_RADIUS) * j
                y = small_lefttop[1] + int(SMALL_GAP + SMALLVIAL_RADIUS) * i
                cv2.circle(self.workspace, (x, y), int(SMALLVIAL_RADIUS), (0, 0, 0))
                SMALL_VIAL_LIST.append([y, x])
                SMALL_VIAL_DICT.update({'small_{}_{}'.format(i-1, j-1): [y, x]})

        #SENSOR
        self.sensor_lefttop_list = []
        self.sensor_rightbottom_list = []

        for i in range(6):
            sensor_lefttop = (int(MARGIN + i * (GAP_ASSAY + SENSOR_WIDTH)), int(self.height - MARGIN - MIDBEDSIZE_HEIGHT - GAP_BED - SENSOR_HEIGHT))
            sensor_rightbottom = (int(MARGIN + SENSOR_WIDTH + i * (GAP_ASSAY + SENSOR_WIDTH)), int(self.height - MARGIN - MIDBEDSIZE_HEIGHT - GAP_BED))
            self.workspace = cv2.rectangle(self.workspace, sensor_lefttop, sensor_rightbottom, (0, 0, 0), 2)
            self.sensor_lefttop_list.append(sensor_lefttop)
            self.sensor_rightbottom_list.append(sensor_rightbottom)


        for k in range(6): #sensor number
            for i in range(1, 9):
                for j in range(1, 3):
                    x = self.sensor_lefttop_list[k][0] + int(SENSOR_GAP + SENSOR_RADIUS) * j
                    y = self.sensor_lefttop_list[k][1] + int(SENSOR_GAP + SENSOR_RADIUS) * i
                    cv2.circle(self.workspace, (x, y), int(SENSOR_RADIUS), (0, 0, 0))
                    SENSOR_VIAL_LIST.append([k, y, x])
                    SENSOR_VIAL_DICT.update({'sensor_{}_{}_{}'.format(k, i-1, j-1): [y, x]})



class RoboticArm(Workspace):
    def __init__(self):
        super(RoboticArm, self).__init__()

        link1_point1 = (int(WORKSPACE_WIDTH - MARGIN), int(MARGIN))
        link1_point2 = (int(WORKSPACE_WIDTH - MARGIN), int(WORKSPACE_HEIGHT - MARGIN))
        cv2.line(self.workspace, link1_point1, link1_point2, (255, 0, 0), 20) #B G R

        link2_point1 = (int(MARGIN), int(MARGIN))
        link2_point2 = (int(WORKSPACE_WIDTH - MARGIN), int(MARGIN))
        # cv2.line(self.workspace, link2_point1, link2_point2, (0, 255, 0), 20)

        link3_point1 = (int(WORKSPACE_WIDTH - MARGIN), int(MARGIN))
        link3_point2 = (int(WORKSPACE_WIDTH - MARGIN), int(MARGIN + A2))
        # cv2.line(self.workspace, link3_point1, link3_point2, (0, 0, 255), 20)
        # cv2.circle(self.workspace, link3_point2, int(SENSOR_RADIUS), 10)

        self.p_start = [link3_point2[0], link3_point2[1]] #[x, y]
        self.SourceTargetToPoint()
        self.visualization()

    def SourceTargetToPoint(self):
        sourcetargetdict = GUI_order.SOURCE_TARGET_AMOUNT_DICT
        for source in sourcetargetdict:
            if source in MID_VIAL_DICT:
                p_source = MID_VIAL_DICT[source]
            elif source in LARGE_VIAL_DICT:
                p_source = LARGE_VIAL_DICT[source]
            elif source in SMALL_VIAL_DICT:
                p_source = SMALL_VIAL_DICT[source]
            elif source in SENSOR_VIAL_DICT:
                p_source = SENSOR_VIAL_DICT[source]
            for target in sourcetargetdict[source]:
                key_target = target[0]
                amount_target = target[1]
                if key_target in MID_VIAL_DICT:
                    p_target = MID_VIAL_DICT[key_target]
                elif key_target in LARGE_VIAL_DICT:
                    p_target = LARGE_VIAL_DICT[key_target]
                elif key_target in SMALL_VIAL_DICT:
                    p_target = SMALL_VIAL_DICT[key_target]
                elif key_target in SENSOR_VIAL_DICT:
                    p_target = SENSOR_VIAL_DICT[key_target]

                WORKPROCESS_LIST.append([p_source, p_target, amount_target])

    def visualization(self):
        p_start = self.p_start.copy()
        link2_x1 = int(MARGIN)
        link2_x2 = int(WORKSPACE_WIDTH - MARGIN)

        work_y = int(MARGIN)
        work_x = int(WORKSPACE_WIDTH - MARGIN)

        dstImg = self.workspace.copy()
        amount = 0.0001
        for worklist in WORKPROCESS_LIST: #[y, x] for worklist
            for i in range(len(worklist) - 1):
                time.sleep(0.5 * amount)
                y_movement = worklist[i][0] - work_y - A2
                y_step = y_movement / STEP

                x_movement = worklist[i][1] - work_x
                x_step = x_movement / STEP
                # time.sleep(amount * 0.2)
                amount = worklist[2]

                for j in range(STEP):

                    work_y = int(work_y + y_step)
                    work_x = int(work_x + x_step)
                    link3_y1 = int(work_y)
                    link3_y2 = int(work_y + A2)

                    cv2.line(dstImg, (link2_x1, work_y), (link2_x2, work_y), (0, 255, 0), 20)
                    cv2.line(dstImg, (work_x, link3_y1), (work_x, link3_y2), (0, 0, 255), 10)
                    cv2.circle(dstImg, (work_x, link3_y2), int(SENSOR_RADIUS), 5)
                    if j == STEP - 1:
                        cv2.circle(dstImg, (worklist[i][1], worklist[i][0]), int(SENSOR_RADIUS + 1), (255, 0, 0), -1)
                    cv2.imshow("dstImg", dstImg)
                    dstImg = self.workspace.copy()
                    time.sleep(0.7)

                    cv2.waitKey(30)

        time.sleep(3)

        BackToFirst()

class BackToFirst(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.windows = list()
        self.back_to_first()

    def back_to_first(self):
        app = QApplication(sys.argv)
        window = GUI_controller.Controller()
        self.windows.append(window)
        GUI_controller.CHECKEDLIST = []
        window.show()
        exit(app.exec_())


def main():
    space = RoboticArm()


if __name__ == "__main__":
    main()


