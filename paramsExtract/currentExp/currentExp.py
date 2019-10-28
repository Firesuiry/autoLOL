import cv2 as cv
import numpy as np

#���뵱ǰ����ֵͼƬ �������ǰ����ٷֱ�


def current_exp(m1):
    hsv = cv.cvtColor(m1, cv.COLOR_BGR2HSV)
    # �趨��ɫ����
    lower_hsv = np.array([125, 80, 70])
    upper_hsv = np.array([155, 255, 255])
    mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    #����ѭ����Ѱ�ҵ�ǰ������ߵ㣬����ɱ���
    count = 0
    for i in range(mask.shape[0]):
        if count == 0:
            for j in range(mask.shape[1]):
                if mask[i, j] != 0:
                    count = i
                    currentExp = (mask.shape[0] - count) / mask.shape[0]
                    print("currentExp:%f" % (currentExp))
                    break
        else:
            break

