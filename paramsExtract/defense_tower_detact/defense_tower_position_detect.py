import cv2,os
import numpy as np

PATH = os.path.split(__file__)[0] + '/'

class targetDetacter():
    def __init__(self):
        self.enemy_neita_target_full = cv2.imread(PATH + 'enemy_neita.png')
        self.ally_neita_target_full = cv2.imread(PATH + 'ally_neita.png')
        self.neita_mask_full = cv2.imread(PATH + 'neita_mask.png')

        self.enemy_waita_target_full = cv2.imread(PATH + 'enemy_waita.png')
        self.ally_waita_target_full = cv2.imread(PATH + 'ally_waita.png')
        self.waita_mask_full = cv2.imread(PATH + 'waita_mask.png')

    @staticmethod
    def colorClear(img):
        img[np.where(np.sum(img, axis=2) < 120)] = [0, 0, 0]
        img[np.where((np.max(img, axis=2) - np.min(img, axis=2) < 25) & (np.sum(img, axis=2) < 300))] = [0, 0, 0]
        return img


    @staticmethod
    def neita_color_check(img, postions, blue=False, red=False):  # 小兵位置调整？？
        new_postions = []
        for pos in postions:

            color = img[pos[1] + 4, pos[0] + 4:pos[0] + 7, :]

            b = color[:, 0]
            g = color[:, 1]
            r = color[:, 2]

            right_bool = False

            if blue:
                right_bool = (((b > r) * (b > g) * (b > 150)) > 0).any()
            if red:
                right_bool = (((r > b) * (r > g) * (r > 150)) > 0).any()

            if right_bool:
                new_postions.append(pos)

        return new_postions

    @staticmethod
    def waita_color_check(img, postions, blue=False, red=False):
        new_postions = []
        for pos in postions:

            color = img[pos[1] + 7, pos[0] + 7:pos[0] + 10, :]

            b = color[:, 0]
            g = color[:, 1]
            r = color[:, 2]

            right_bool = False

            if blue:
                right_bool = (((b > r) * (b > g) * (b > 150)) > 0).any()
            if red:
                right_bool = (((r > b) * (r > g) * (r > 150)) > 0).any()

            if right_bool:
                new_postions.append(pos)

        return new_postions


    @staticmethod
    def findPics(oriImg, targetImg, mask=None, threshold=0.8, test='', color=[255, 0, 0],
                 maxThreshold=1.1):  # 返回了目标模板左上角的坐标
        h, w = targetImg.shape[:2]  # rows->h, cols->w
        h2, w2 = oriImg.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)

        img = oriImg.copy()

        postions = []

        while (True):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            horizen0 = np.max([0, max_loc[1] - h // 2])
            horizen1 = np.min([h2, max_loc[1] + h // 2])
            vertical0 = np.max([0, max_loc[0] - w // 2])
            vertical1 = np.min([w2, max_loc[0] + w // 2])

            if max_val > threshold and max_val < maxThreshold:
                left_top = max_loc  # 左上角
                right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
                if test is not '':
                    cv2.rectangle(img, left_top, right_bottom, (0, 0, 255), 2)  # 将匹配区域绘制到原图上
                postions.append(left_top)
            elif max_val <= threshold:
                break
            res[horizen0:horizen1, vertical0:vertical1] = 0

        if test is not '':
            cv2.imwrite('result{}.png'.format(test), img)

        return np.array(postions)

    def getTargetPostions(self, img):
        dic = {}
        img0 = img.copy()
        img0 = self.colorClear(img0)
        enemy_neita_postions = self.findPics(img0, self.enemy_neita_target_full, self.neita_mask_full,
                                             threshold=0.95,
                                             color=[255, 255, 255])
        ally_neita_postions = self.findPics(img0, self.ally_neita_target_full, self.neita_mask_full,
                                            threshold=0.95,
                                            color=[255, 255, 255])
        enemy_waita_postions = self.findPics(img0, self.enemy_waita_target_full, self.waita_mask_full,
                                             threshold=0.95,
                                             color=[255, 255, 255])
        ally_waita_postions = self.findPics(img0, self.ally_waita_target_full, self.waita_mask_full,
                                            threshold=0.95,
                                            color=[255, 255, 255])
        new_ally_neita_postions = self.neita_color_check(img0, ally_neita_postions, blue=True)
        new_enemy_neita_postions = self.neita_color_check(img0, enemy_neita_postions, red=True)
        new_ally_waita_postions = self.waita_color_check(img0, ally_waita_postions, blue=True)
        new_enemy_waita_postions = self.waita_color_check(img0, enemy_waita_postions, red=True)

        dic['ally_neita'] = new_ally_neita_postions
        dic['enemy_neita'] = new_enemy_neita_postions
        dic['ally_waita'] = new_ally_waita_postions
        dic['enemy_waita'] = new_enemy_waita_postions

        return dic

    def Final_Postions(self, img):
        d1 = np.array([50,150])
        d2 = np.array([110,160])
        ally_tower_postion = []
        enemy_tower_position = []
        target_postion = self.getTargetPostions(img)
        ally_neita_postion = target_postion['ally_neita']
        enemy_neita_postion = target_postion['enemy_neita']
        ally_waita_postion = target_postion['ally_waita']
        enemy_waita_postion = target_postion['enemy_waita']
        for pos in ally_neita_postion:
            pos = pos + d1
            ally_tower_postion.append(pos)
        for pos in enemy_neita_postion:
            pos = pos + d1
            enemy_tower_position.append(pos)
        for pos in ally_waita_postion:
            pos = pos + d2
            ally_tower_postion.append(pos)
        for pos in enemy_waita_postion:
            pos = pos + d2
            enemy_tower_position.append(pos)
        return ally_tower_postion,enemy_tower_position

tower_detacter = targetDetacter()

if __name__ == '__main__':
    for i in range(1, 10):
        index = i * 267 + 231
        img0 = cv2.imread(r'D:\ans\game0\{}.png'.format(index))  # 读入图像
        ally_tower_postion, enemy_tower_position = tower_detacter.Final_Postions(img0)
        for pos in ally_tower_postion:
             cv2.circle(img0, tuple(pos), 10, (0, 0, 0), 5)
        for pos in enemy_tower_position:
            cv2.circle(img0, tuple(pos), 10, (255, 255, 255), 5)
        # target_postion = tower_detacter.getTargetPostions(tower_detacter,img0)  # 目标位置
        # d1 = np.array([50,150])
        # d2 = np.array([110,160])
        # ally_neita_postion = target_postion['ally_neita']
        # for pos in ally_neita_postion:
        #     cv2.circle(img0, tuple(pos+d1), 10, (0, 255, 0), 5)
        #
        # enemy_neita_postion = target_postion['enemy_neita']
        # for pos in enemy_neita_postion:
        #     cv2.circle(img0, tuple(pos+d1), 10, (0, 0, 255), 5)
        #
        # ally_waita_postion = target_postion['ally_waita']
        # for pos in ally_waita_postion:
        #     cv2.circle(img0, tuple(pos+d2), 10, (0, 0, 0), 5)
        #
        # enemy_waita_postion = target_postion['enemy_waita']
        # for pos in enemy_waita_postion:
        #     cv2.circle(img0, tuple(pos+d2), 10, (255, 255, 255), 5)
        #     print(pos,type(pos))

        cv2.imwrite('C:/Users/lijixing/Desktop/1/test_img{}.png'.format(i), img0)
