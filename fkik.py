import numpy as np

def fkine(alpha, a, d, theta):
    HT = np.array([[np.cos(theta), -np.sin(theta), 0, a], \
                   [np.sin(theta) * np.cos(alpha), np.cos(theta) * np.cos(alpha), -np.sin(alpha), -np.sin(alpha) * d],\
                   [np.sin(theta) * np.sin(alpha), np.cos(theta) * np.sin(alpha), np.cos(alpha), np.cos(alpha) * d],\
                   [0, 0, 0, 1]])
    return HT

def fkine_DHtable(alphaList, aList, dList, thetaList):
    HTList = np.zeros((len(alphaList), 4, 4))
    print(len(alphaList))
    for i in range(len(alphaList)):
        HT = fkine(alphaList[i], aList[i], dList[i], thetaList[i])
        HTList[i] = HT
    return HTList



