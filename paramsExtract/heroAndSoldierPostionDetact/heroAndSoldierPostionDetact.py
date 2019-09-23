import cv2
import numpy as np
import matplotlib.pyplot as plt

def findPics(oriImg, targetImg, mask , threshold=0.8, delay=0.5, test=False):
    h, w = targetImg.shape[:2]  # rows->h, cols->w
    res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_SQDIFF)
    # res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED,mask)
    #大小展示
    res2 = res.reshape(-1)
    res2 = np.sort(res2)
    print(res2[0:10])




    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    minValue = np.min(res)


    print(minValue)
    if minValue > threshold or True:
        left_top = min_loc  # 左上角
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if test:
            # print(maxValue)
            img = oriImg.copy()
            cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
            cv2.imwrite('result.png', img)
            cv2.imwrite('mask2.png',mask)

        return [left_top, right_bottom]

def findPic2(oriImg, targetImg, mask , threshold=0.8, delay=0.5, test=False):
    point = [0, 0]
    h, w = targetImg.shape[:2]  # rows->h, cols->w
    res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_SQDIFF,mask)
    # res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED,mask)
    #大小展示
    res2 = res.reshape(-1)
    res2 = np.sort(res2)
    print(res2[0:10])




    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    minValue = np.min(res)


    print(minValue)
    if minValue > threshold or True:
        left_top = min_loc  # 左上角
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if test:
            # print(maxValue)
            img = oriImg.copy()
            cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
            cv2.imwrite('result.png', img)
            cv2.imwrite('mask2.png',mask)

        return [left_top, right_bottom]

def findPic(oriImg, targetImg, mask , threshold=0.8, delay=0.5, test=False):
    h, w = targetImg.shape[:2]  # rows->h, cols->w
    res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED,mask =mask)
    # res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED,mask)
    #大小展示
    res2 = res.reshape(-1)
    res2 = np.sort(res2)
    print(res2[-10:-1])




    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    maxValue = np.max(res)
    print(maxValue)
    if maxValue > threshold or True:
        left_top = max_loc  # 左上角
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if test:
            # print(maxValue)
            img = oriImg.copy()
            cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
            cv2.imwrite('result.png', img)
            cv2.imwrite('mask2.png',mask)

        return [left_top, right_bottom]

target = cv2.imread('target.png')
mask = cv2.imread('mask3.png')
img0 = cv2.imread(r'E:\develop\autoLOLres\ans\screen779.bmp')


#print(type(img0))
#print(type(img0[0][0][0]))

#target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
#img0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
#mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#mask = np.uint8(mask<250)
#zero_channel = np.zeros_like(mask)
#transparent_mask = cv2.merge([mask, mask, mask])
#print(transparent_mask[0:5,0:5])

findPic(img0,target,None,test=True)

findPic(img0,target,mask,test=True)


