# -*- coding: utf-8 -*-
from paramsExtract.paramsExtracter import paramExtract
import numpy as np
import cv2
import matplotlib.pyplot as plt
from reviewAndTrain.dataStore import dataStore
from modelManger import model_manager


class picProcessor:
    def __init__(self, op, test=False):
        self.test = test
        self.operater = op
        if not test:
            self.ds = dataStore()

        # 以下初始化一些数据
        self.currentPic = None
        # x0,y0,x1,y1
        self.positionData = {
            'HP': [454, 686, 730, 697],
            'MP': [454, 699, 730, 710],
            'MONEY': [798, 696, 860, 712],
            'MAP': [1100, 538, 1279, 719],
            'EXP': [410, 622, 448, 710]
        }

        # 节点名称介绍
        """
        首位 L左下边 R右上边
        次位 Base基地（结束） T上 M中 B下
        再次 Node 召唤节点（结束） T塔 R河道边
        再次 1高地塔（结束） 2二塔（结束） 3边塔（结束） 0门牙塔
        再次 0左门牙塔（结束） 1右门牙塔（结束）
        """
        self.nodesPostions = {
            'LSpring': [1105, 707],
            'LBase': [1119, 694],
            'LBNode': [1142, 699],
            'LBT1': [1151, 700],
            'LBT2': [1182, 697],
            'LBT3': [1223, 700],
            'LBR': [1243, 692],
            'RBR': [1254, 680],
            'RBT3': [1262, 633],
            'RBT2': [1256, 619],
            'RBT1': [1260, 592],
            'RBNode': [1259, 583],
            'RT01': [1253, 568],
            'RT00': [1247, 563],
            'RBase': [1255, 560],
        }
        self.bottomNodeKeys = ['LSpring', 'LBase', 'LBNode', 'LBT1', 'LBT2', 'LBT3', 'LBR', 'RBR', 'RBT3', 'RBT2',
                               'RBT1', 'RBNode', 'RT01', 'RT00', 'RBase']
        # 数据处理
        self.bottimMiddlePoint = []
        point = np.array([0, 0])
        for key in self.bottomNodeKeys:
            newPoint = np.array(self.nodesPostions[key])
            if (point == 0).all():
                point = newPoint
            else:
                middlePoint = 0.5 * (point + newPoint)
                point = newPoint
                self.bottimMiddlePoint.append(middlePoint)

        # 创建节点列表
        self.bottomNodeList = []
        for key in self.bottomNodeKeys:
            self.bottomNodeList.append(self.nodesPostions[key])

        # 节点插值
        assert len(self.bottomNodeList) != 0
        self.newBottomNodeList = []
        for node in self.bottomNodeList:
            node = np.array(node)
            if len(self.newBottomNodeList) == 0:
                self.newBottomNodeList.append(node)
                continue
            middlePoint = (self.newBottomNodeList[-1] + node) * 0.5
            self.newBottomNodeList.append(middlePoint)
            self.newBottomNodeList.append(node)
        self.bottomNodeList = self.newBottomNodeList.copy()
        assert (len(self.bottomNodeList) != 0)

    def element_extract(self, element_name, ori_pic):
        """
        从图片中提取某些元素，如小地图，血条，蓝条等，具体数据在self.postionData
        :param element_name: 元素名称 具体看那个字典
        :param ori_pic: 原始图片 格式cv2图片
        :return: 返回地图，格式cv2图片
        """

        # print ('element_extract elment:{}'.format(elementName))
        targetArea = self.positionData.get(element_name, None)
        assert targetArea is not None
        pic = ori_pic[targetArea[1]:targetArea[3], targetArea[0]:targetArea[2]]
        # print(pic.shape)
        return pic

    @staticmethod
    def pic_display(pic, save_name='', pil=False, no_dis=False):
        if np.max(pic) <= 1:
            pic = pic * 255
        if not no_dis:
            if not pil:
                cv2.imshow('pic', pic)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                plt.figure(save_name)
                plt.imshow(pic)
                plt.show()
        if save_name != '':
            cv2.imwrite('ans/' + save_name + '.png', pic)

    def point_transform(self, point_in, map2all=False):
        """
        :param point_in: 输入坐标，【X，Y】
        :param map2all: 如果是小地图转通用坐标，该参数为True
        :return:返回坐标值列表，【y，x】
        """
        point_in = point_in.copy()
        yOffset = self.positionData['MAP'][0]
        xOffset = self.positionData['MAP'][1]
        addRatio = -1
        if map2all:
            addRatio = 1
        point_in[0] += addRatio * yOffset
        point_in[1] += addRatio * xOffset
        return point_in

    def param_extract(self, img, game_running=True):
        assert (img.shape == (720, 1280, 3))
        same = (img == self.currentPic).all()
        print('获取图片 重复判断结果：{}'.format(same))
        if same:
            return
        self.currentPic = img
        return paramExtract(self, game_running)

    def get_pic(self, pic: np.ndarray, test=False):
        """
        获取图片的函数，图片从此开始处理
        :param test:是否处于非游戏状态
        :param pic:游戏全图
        :return:
        """

        # 获取OB
        assert (pic.shape == (720, 1280, 3))
        same = (pic == self.currentPic).all()
        print('获取图片 重复判断结果：{}'.format(same))
        if same:
            return
        self.currentPic = pic
        errorTimes = 0
        if not test:
            try:
                # OB加工
                params = paramExtract(self)
                # 动作选择
                action = self.determine_action(params)
                targetAction = self.operater.actionExcute(action, params)

                # 动作保存
                self.ds.storeResult(pic, params, targetAction)
                errorTimes = 0
            except Exception as e:
                print("图片处理错误，详情：{}".format(e))
                errorTimes += 1
                if errorTimes > 10:
                    raise ()
                return -1
        else:
            params = paramExtract(self, False)
            action = self.determine_action(params)
            print('action:')
            print(action)
            print('params')
            print(params)


if __name__ == "__main__":
    pass

