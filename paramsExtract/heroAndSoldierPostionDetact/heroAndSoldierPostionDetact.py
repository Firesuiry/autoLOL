import math
import cv2
import numpy as np
import time
try:
    from setting import *
    from modelManger import model_manager
except Exception as e:
    PROJECT_ADDRESS = ''


class targetDetacter():
    def __init__(self):
        if PROJECT_ADDRESS is not '':
            self.path = PROJECT_ADDRESS + r'paramsExtract/heroAndSoldierPostionDetact/'
        else:
            self.path = ''
        self.hero_target = cv2.imread(self.path + 'target.png')
        self.hero_mask = cv2.imread(self.path + 'mask3.png')

        self.enemy_soldier_target_full = cv2.imread(self.path + 'xiaobingHP.png')
        self.ally_soldier_target_full = cv2.imread(self.path + 'soldier_hp_self.png')
        print(self.ally_soldier_target_full.shape)
        self.ally_soldier_target_full = self.colorClear(self.ally_soldier_target_full)
        self.enemy_soldier_target_full = self.colorClear(self.enemy_soldier_target_full)
        self.soldier_mask_full = cv2.imread(self.path + 'xiaobingHP_mask_l.png')

    def get_target_mat(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mat = model_manager.useModel('ally_detacter.h5', img.reshape(1,720,1280,3))
        return mat

    @staticmethod
    def colorClear(img):
        img[np.where(np.sum(img, axis=2) < 120)] = [0, 0, 0]
        img[np.where((np.max(img,axis= 2) - np.min(img,axis=2) < 25 )&( np.sum(img, axis=2) < 300))] = [0,0,0]
        return img


    @staticmethod
    def soldier_color_check(img, postions, blue = False, red = False):
        new_postions = []
        for pos in postions:
            x = pos[0] + 1
            y = pos[1] + 1

            color = img[pos[1]+1:pos[1] + 4,pos[0]+1,:]


            # cv2.imwrite('f.png',color)
            # print(img.shape)
            # print(color.shape)
            b = color[:,0]
            g = color[:,1]
            r = color[:,2]
            right_bool = False

            if blue:
                right_bool = (((b > r) * (b > g) * (b > 150)) > 0).any()
            if red:
                right_bool = (((r > b) * (r > g) * (r > 100)) > 0).any()

            if right_bool:
                new_postions.append(pos)

        return new_postions

    @staticmethod
    def hero_color_check(img, postions):
        new_postions = []
        for pos in postions:
            x = pos[0] + 1
            y = pos[1] + 1

            color = img[pos[1] + 20:pos[1] + 23, pos[0] + 27, :]
            # cv2.imwrite('f.png',img[pos[1]+20:pos[1] + 23, pos[0]+27:pos[0] + 50, :])

            b = color[:,0]
            g = color[:,1]
            r = color[:,2]
            right_bool = False

            right_bool = (((b > r) * (b > g) * (b > 100)) > 0).any()

            color0 = img[pos[1]:pos[1] + 20, pos[0]:pos[0]+20, :]

            color = np.sum(color0,axis=2)
            right_bool2 = np.max(color) > 600


            right_bool = right_bool and right_bool2
            if right_bool:
                # cv2.imwrite('pic/{}f{}-{}.png'.format(right_bool2, pos,np.max(color)), color0)
                new_postions.append(pos)

        return new_postions

    def getTargetPostions(self,img,ally_soldier = True,enemy_soldier = True,heros = True, return_as_ndarry = False):
        dic = {}
        if heros:
            hero_postions = self.findPics(img, self.hero_target, self.hero_mask, threshold=0.96, color=[0, 0, 255])
            new_heros_postion = np.array(self.hero_color_check(img, hero_postions))
            if new_heros_postion.shape[0] != 0:
                new_heros_postion += (67, 95)
            dic['hero'] = new_heros_postion

        if ally_soldier or enemy_soldier:
            ori_img = img.copy()
            ori_img = self.colorClear(ori_img)

            if ally_soldier:
                ally_soldier_postions = self.findPics(ori_img, self.ally_soldier_target_full, self.soldier_mask_full,
                                                      threshold=0.85, color=[255, 255, 255])
                new_ally_soldier_postions = np.array(self.soldier_color_check(ori_img, ally_soldier_postions, blue=True))
                if new_ally_soldier_postions.shape[0] != 0:
                    new_ally_soldier_postions += (34, 36)
                dic['ally_soldier'] = new_ally_soldier_postions

            if enemy_soldier:
                enemy_soldier_postions = self.findPics(ori_img, self.enemy_soldier_target_full, self.soldier_mask_full,
                                                       threshold=0.85, color=[255, 255, 255])
                new_enemy_soldier_postions = np.array(self.soldier_color_check(ori_img, enemy_soldier_postions, red=True))
                if new_enemy_soldier_postions.shape[0] != 0:
                    new_enemy_soldier_postions += (34, 36)
                dic['enemy_soldier'] = new_enemy_soldier_postions
        if not return_as_ndarry or not ally_soldier or not enemy_soldier or not heros:
            return dic
        else:
            nd = [dic['ally_soldier'], dic['enemy_soldier'], dic['hero']]
            return np.array(nd)

    @staticmethod
    def findPics(oriImg, targetImg, mask = None, threshold=0.8, test='',color = [255, 0, 0] , maxThreshold = 1.1):
        # print(oriImg.shape)
        h, w = targetImg.shape[:2]  # rows->h, cols->w
        h2, w2 = oriImg.shape[:2]  # rows->h, cols->w
        res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)
        img = oriImg.copy()
        # img = oriImg
        postions = []
        while(True):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            #找出来以后 loc的左边顺序是反的

            horizen0 = np.max([0,max_loc[1]-h//2])
            horizen1 = np.min([h2,max_loc[1]+h//2])
            vertical0 = np.max([0,max_loc[0]-w//2])
            vertical1 = np.min([w2,max_loc[0]+w//2])

            if max_val > threshold and max_val < maxThreshold:
                left_top = max_loc  # 左上角
                right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
                if test is not '':
                    cv2.rectangle(img, left_top, right_bottom, color, 1)  # 画出矩形位置
                postions.append(left_top)
            elif max_val <= threshold:
                break
            res[horizen0:horizen1,vertical0:vertical1] = 0
        if test is not '':
            cv2.imwrite('result{}.png'.format(test), img)

        return np.array(postions)


    @staticmethod
    def gezi(img,space):
        w,h = img.shape[:2]
        for i in range(h // space):
            cv2.line(img,(space*(i+1),0),(space*(i+1),w-1),(255,255,255))

        for i in range(w // space):
            cv2.line(img,(0,space*(i+1)),(h-1,space*(i+1)),(255,255,255))
        print('总格数：',h // space * (h // space))
        return img

hero_soldier_detacter = targetDetacter()

def test():
    img0 = cv2.imread(r'ori2.png')

    target_postion = hero_soldier_detacter.getTargetPostions(img0)
    ally_postion = target_postion['ally_soldier']
    img0 = cv2.imread(r'ori2.png')
    for pos in ally_postion:
        cv2.circle(img0, tuple(pos), 15, (255, 0, 255), 5)
    enemy_postion = target_postion['enemy_soldier']
    for pos in enemy_postion:
        cv2.circle(img0, tuple(pos), 5, (0, 255, 255), 5)
    hero_postion = target_postion['hero']
    for pos in hero_postion:
        cv2.circle(img0, tuple(pos), 10, (255, 255, 0), 5)
        # img0[pos[1],pos[0]] = (255, 255, 0)
    cv2.imwrite('pic/test_img.png', img0)

    h, w, c = img0.shape
    h = math.ceil(h / 32) - 1
    w = math.ceil(w / 32)
    unit_mat = np.zeros((3, h, w), dtype=int)
    all_potions = [ally_postion,enemy_postion,hero_postion]
    for i in range(3):
        for pos in all_potions[i]:
            x = pos[0] // 32
            y = pos[1] // 32
            print(pos, x, y)
            if y > 21:
                y = 21
            unit_mat[i, y, x] = 1

    for k in range(3):
        for i in range(unit_mat[k].shape[0]):
            for j in range(unit_mat[k].shape[1]):
                if unit_mat[k][i, j] > 0.5:
                    left_top = (j*32,i*32)
                    right_bottom = (j*32+32,i*32+32)
                    cv2.rectangle(img0, left_top, right_bottom, (255*(k == 0),255*(k == 1),255*(k == 2)), 2)
    cv2.imwrite('pic/test_img2.png',img0)
    unit_mat = np.swapaxes(unit_mat, 0, 2)
    unit_mat = np.swapaxes(unit_mat, 0, 1)
    cv2.imwrite('pic/test_img3.png', unit_mat*255)


if __name__ == '__main__':
    test()
    exit()

    start = time.time()
    for i in range(8):
        index = i * 1000 + 53
        img0 = cv2.imread(r'D:\develop\autoLOL\ans\game0\{}.png'.format(index))
        # img0 = cv2.imread(r'0.png')
        target_postion = hero_soldier_detacter.getTargetPostions(img0)
        ally_postion = target_postion['ally_soldier']
        img0 = cv2.imread(r'D:\develop\autoLOL\ans\game0\{}.png'.format(index))
        # img0 = cv2.imread(r'0.png')
        for pos in ally_postion:
            cv2.circle(img0,tuple(pos),15,(255,0,255),5)
        enemy_postion = target_postion['enemy_soldier']
        for pos in enemy_postion:
            cv2.circle(img0,tuple(pos),5,(0,255,255),5)
        hero_postion = target_postion['hero']
        for pos in hero_postion:
            cv2.circle(img0,tuple(pos),10,(255,255,0),5)

        cv2.imwrite('pic/test_img{}.png'.format(index),targetDetacter.gezi(img0,32))
    need_time = time.time() - start
    print('花费时间:{} 平均每个：{}'.format(need_time,need_time/8))
