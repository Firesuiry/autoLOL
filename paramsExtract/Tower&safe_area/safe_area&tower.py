# _author_='ZZQ';
# date: 2019/11/29 0029 ;

import cv2 as cv
import numpy as np


# 识别目标
def tempalte_demo(begining_image):
    begining_result = cv.imread("C:/Users/Administrator/Desktop/dataset/1.png")
    # 二值化
    hsv_result = cv.cvtColor(begining_result, cv.COLOR_BGR2HSV)
    hsv_image = cv.cvtColor(begining_image, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([100, 160, 205])
    upper_hsv = np.array([110, 175, 255])
    after_result = cv.inRange(hsv_result, lowerb=lower_hsv, upperb=upper_hsv)
    after_image = cv.inRange(hsv_image, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('3', after_image)

    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = after_result.shape[:2]
    A = np.zeros((after_image.shape[0], after_image.shape[1]))
    for md in methods:
        result = cv.matchTemplate(after_image, after_result, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            t1 = min_loc
        else:
            t1 = max_loc
        br = (t1[0] + tw, t1[1] + th)
        A[int((t1[0]+br[0])/2), int((t1[1]+br[1])/2)] = 1
        # image = cv.circle(begining_image, (int((t1[0]+br[0])/2), int((t1[1]+br[1])/2)), 1, (0, 0, 0), 25)
        # cv.imshow('rect', image)
        finialresult = cv.rectangle(after_image, t1, br, (255, 255, 255), 2)
    return finialresult


# 根据要识别的颜色，处理图像为黑白。二值化
def image_extrator(m1):
    hsv = cv.cvtColor(m1, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([35, 0, 75])
    upper_hsv = np.array([150, 255, 255])
    mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    return mask


def erode(img):
    kernel = np.ones((2, 2))
    img = cv.erode(img, kernel)
    return img


# 下路最远安全位置
def far_safe_area(img):

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([35, 0, 75])
    upper_hsv = np.array([150, 255, 255])
    mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('', mask)
    A = mask
    B = A[:150, 158].reshape(150, 1)
    C = A[160, :160].reshape(1, 160)
    if np.sum(B) > (B.shape[1]*B.shape[0]*255*0.005):
        for i in range(0, B.shape[0]):
            if B[i, 0] != 0:
                local = (i+20, 158)
                break
    else:
        for i in reversed(range(0, C.shape[1])):
            if C[0, i] != 0:
                local = (160, i-15)
                break
    return local


# 识别我方镀层塔
def recognition_our_tower(begining_image):
    begining_result = cv.imread("C:/Users/Administrator/Desktop/dataset/41.png")
    # 二值化
    hsv_result = cv.cvtColor(begining_result, cv.COLOR_BGR2HSV)
    hsv_image = cv.cvtColor(begining_image, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([90, 160, 80])
    upper_hsv = np.array([100, 185, 255])
    after_result = cv.inRange(hsv_result, lowerb=lower_hsv, upperb=upper_hsv)
    after_image = cv.inRange(hsv_image, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('ab', after_image)

    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = after_result.shape[:2]
    A = np.zeros((after_image.shape[0], after_image.shape[1]))
    Ts = []
    for md in methods:
        result = cv.matchTemplate(after_image, after_result, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            t1 = min_loc
        else:
            t1 = max_loc
        br = (t1[0] + tw, t1[1] + th)
        A[int((t1[0] + br[0]) / 2), int((t1[1] + br[1]) / 2)] = 1
        # image = cv.circle(begining_image, (int((t1[0]+br[0])/2), int((t1[1]+br[1])/2)), 1, (0, 0, 0), 25)
        # cv.imshow('rect', image)
        finialresult = cv.rectangle(after_image, t1, br, (255, 255, 255), 2)
        T = (int((t1[1]+br[1])/2), int((t1[0]+br[0])/2))

        if contain(Ts, T) == 1:
            break
        else:
            Ts.append(T)

    # cv.imshow('target', finialresult)

    return Ts


# 识别我方没有镀层塔
def recognition_normal_our_tower(begining_image):
    begining_result = cv.imread("C:/Users/Administrator/Desktop/dataset/42.png")
    # 二值化
    hsv_result = cv.cvtColor(begining_result, cv.COLOR_BGR2HSV)
    hsv_image = cv.cvtColor(begining_image, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([90, 100, 80])
    upper_hsv = np.array([100, 185, 205])
    after_result = cv.inRange(hsv_result, lowerb=lower_hsv, upperb=upper_hsv)
    after_image = cv.inRange(hsv_image, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('3', after_image)

    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED,
               cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED,
               cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = after_result.shape[:2]
    A = np.zeros((after_image.shape[0], after_image.shape[1]))
    Ts = []
    for md in methods:
        result = cv.matchTemplate(after_image, after_result, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            t1 = min_loc
        else:
            t1 = max_loc
        br = (t1[0] + tw, t1[1] + th)
        A[int((t1[0] + br[0]) / 2), int((t1[1] + br[1]) / 2)] = 1
        # image = cv.circle(begining_image, (int((t1[0]+br[0])/2), int((t1[1]+br[1])/2)), 1, (0, 0, 0), 25)
        # cv.imshow('rect', image)
        finialresult = cv.rectangle(after_image, t1, br, (255, 255, 255), 2)
        T = (int((t1[1]+br[1])/2), int((t1[0]+br[0])/2))

        if contain(Ts, T) == 1:
            break
        else:
            Ts.append(T)

    # cv.imshow('normal', finialresult)
    return Ts


# 识别敌方没有镀层塔
def recognition_normal_enemy_tower(begining_image):

    begining_result = cv.imread("C:/Users/Administrator/Desktop/dataset/43.png")
    # 二值化
    hsv_result = cv.cvtColor(begining_result, cv.COLOR_BGR2HSV)
    hsv_image = cv.cvtColor(begining_image, cv.COLOR_BGR2HSV)

    # setting color interval
    lower_hsv = np.array([0, 100, 50])
    upper_hsv = np.array([10, 255, 255])
    after_result = cv.inRange(hsv_result, lowerb=lower_hsv, upperb=upper_hsv)
    after_image = cv.inRange(hsv_image, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('22', after_image)

    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED,
               cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED,
               cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = after_result.shape[:2]
    A = np.zeros((after_image.shape[0], after_image.shape[1]))
    Ts = []
    for md in methods:
        result = cv.matchTemplate(after_image, after_result, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            t1 = min_loc
        else:
            t1 = max_loc
        br = (t1[0] + tw, t1[1] + th)
        A[int((t1[0] + br[0]) / 2), int((t1[1] + br[1]) / 2)] = 1
        finialresult = cv.rectangle(after_image, t1, br, (255, 255, 255), 2)
        T = (int((t1[1]+br[1])/2), int((t1[0]+br[0])/2))

        if contain(Ts, T) == 1:
            break
        else:
            Ts.append(T)
    # cv.imshow('ret', finialresult)
    return Ts


# 识别敌方镀层塔
def recognition_enemy_tower(begining_image):
    begining_result = cv.imread("C:/Users/Administrator/Desktop/dataset/44.png")
    # 二值化
    hsv_result = cv.cvtColor(begining_result, cv.COLOR_BGR2HSV)
    hsv_image = cv.cvtColor(begining_image, cv.COLOR_BGR2HSV)
    # setting color interval
    lower_hsv = np.array([0, 150, 50])
    upper_hsv = np.array([10, 255, 255])
    after_result = cv.inRange(hsv_result, lowerb=lower_hsv, upperb=upper_hsv)
    after_image = cv.inRange(hsv_image, lowerb=lower_hsv, upperb=upper_hsv)
    # cv.imshow('ab', after_image)

    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCOEFF_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = after_result.shape[:2]
    A = np.zeros((after_image.shape[0], after_image.shape[1]))
    Ts = []
    for md in methods:
        result = cv.matchTemplate(after_image, after_result, md)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            t1 = min_loc
        else:
            t1 = max_loc
        br = (t1[0] + tw, t1[1] + th)
        A[int((t1[0] + br[0]) / 2), int((t1[1] + br[1]) / 2)] = 1
        # image = cv.circle(begining_image, (int((t1[0]+br[0])/2), int((t1[1]+br[1])/2)), 1, (0, 0, 0), 25)
        # cv.imshow('rect', image)
        finialresult = cv.rectangle(after_image, t1, br, (255, 255, 255), 2)
        T = (int((t1[1] + br[1]) / 2), int((t1[0] + br[0]) / 2))

        if contain(Ts, T) == 1:
            break
        else:
            Ts.append(T)

    # cv.imshow('target', finialresult)

    return Ts


def contain(A, a):
    for i in range(len(A)):
        if a == A[i]:
            return True
            break
    return False

# 载入图片
begining_image = cv.imread("C:/Users/Administrator/Desktop/dataset/2.png")
# cv.imshow('A', begining_image)

# 二值化

# 测试最远安全坐标
safe_local = far_safe_area(begining_image)
print('下路最远安全位置：'+str(safe_local))

# 测试识别英雄
# cv.imshow('1', cv.imread("C:/Users/Administrator/Desktop/dataset/5.png"))
# target = tempalte_demo(cv.imread("C:/Users/Administrator/Desktop/dataset/5.png"))
# cv.imshow('target', target)

# 识我方镀层塔
tower_our_local = recognition_our_tower(begining_image)
print('我方镀层塔的坐标：'+str(tower_our_local))

# 识别我方不含镀层塔
tower_normal_our_local = recognition_normal_our_tower(begining_image)
print('我方不带镀层塔的坐标：'+str(tower_normal_our_local))

# 识别敌方镀层塔
tower_enemy_local = recognition_enemy_tower(begining_image)
print('敌方镀层塔的坐标：'+str(tower_enemy_local))

# 识别敌方不含镀层塔
tower_normal_emeny_local = recognition_normal_enemy_tower(begining_image)
print('敌方不带镀层塔的坐标：'+str(tower_normal_emeny_local))


# 测试腐蚀效果
# img_erode = erode(after_image)
# cv.imshow('img_erode',img_erode)
cv.waitKey(0)
cv.destroyAllWindows()



