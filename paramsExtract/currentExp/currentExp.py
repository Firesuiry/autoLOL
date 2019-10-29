
import cv2 as cv
import numpy as np

#input current experience  image ,ouput current experience


def current_exp(m1):
    hsv = cv.cvtColor(m1, cv.COLOR_BGR2HSV)

    # setting color interval
    lower_hsv = np.array([125, 80, 70])
    upper_hsv = np.array([155, 255, 255])
    mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)

    #make a = new extracted matrix
    a = np.amax(mask,1)
    sum = np.sum(a)

    #return current experience proportion
    if sum>=16*255 :
       return(round(((sum+16*255)/(255*a.shape[0])),2))
    else:
        return 0
