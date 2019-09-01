import numpy as np
import cv2
from skimage import morphology
from sklearn.cluster import MeanShift
from operater import operater
import time

class postionClass():
    def __init__(self):
        pass

    #节点名称介绍
    '''
    首位 L左下边 R右上边
    次位 Base基地（结束） T上 M中 B下
    再次 Node 召唤节点（结束） T塔 R河道边
    再次 1高地塔（结束） 2二塔（结束） 3边塔（结束） 0门牙塔
    再次 0左门牙塔（结束） 1右门牙塔（结束）
    '''

    @staticmethod
    def LBase():
        return [1119,694]

    @staticmethod
    def LBNode():
        return [1142,699]

    @staticmethod
    def LBT1():
        return [1151,700]

    @staticmethod
    def LBT2():
        return [1182,697]

    @staticmethod
    def LBT3():
        return [1223,700]

    @staticmethod
    def RBT3():
        return [1262,633]

    @staticmethod
    def RBT2():
        return [1256,619]

    @staticmethod
    def RBT1():
        return [1260,592]

    @staticmethod
    def RBNode():
        return [1259,583]

    @staticmethod
    def RBase():
        return [1255,560]

    @staticmethod
    def RT00():
        return [1247,563]

    @staticmethod
    def RT01():
        return [1253,568]

class picProcesser():
    def __init__(self):
        self.operater = operater()

        self.dataInit()

    def dataInit(self):
        '''
        init the data which is need in the processer
        :return:None
        '''
        self.currentPic = None
        #x0,y0,x1,y1
        self.postionData = {
            'HP':[515,697,700,705],
            'MP':[515,706,700,714],
            'MONEY':[715,703,794,716],
            'CS':[1184,3,1217,20],#补刀
            'MAP':[538,1100,719,1279]
        }
        self.nodesPostions = {
            'LBase':[1119,694],
            'LBNode':[1142, 699],
            'LBT1':[1151, 700],
            'LBT2':[1182, 697],
            'LBT3':[1223, 700],
            'LBR':[1243,692],
            'RBR':[1254,680],
            'RBT3':[1262, 633],
            'RBT2':[1256, 619],
            'RBT1':[1260, 592],
            'RBNode':[1259, 583],
            'RT01':[1253, 568],
            'RT00':[1247, 563],
            'RBase':[1255, 560],
        }
        self.bottomNodeKeys = ['LBase', 'LBNode', 'LBT1', 'LBT2', 'LBT3','LBR','RBR', 'RBT3', 'RBT2', 'RBT1', 'RBNode', 'RT01', 'RT00', 'RBase']
        #数据处理
        self.bottimMiddlePoint = []
        point = np.array([0,0])
        for key in self.bottomNodeKeys:
            newPoint = np.array(self.nodesPostions[key])
            if (point == 0).all():
                point = newPoint
            else:
                middlePoint = 0.5 * (point + newPoint)
                point = newPoint
                self.bottimMiddlePoint.append(middlePoint)

        #创建节点列表
        self.bottomNodeList = []
        for key in self.bottomNodeKeys:
            self.bottomNodeList.append(self.nodesPostions[key])

        #节点插值
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






    def posCaculate(self,x,y,bottom = False,top = False,middle = False):
        if not (bottom or top or middle):
            bottom = True

        if bottom:
            pos = [x,y]

    def closePointDetact(self,point,pointList):
        '''
        :param point: 输入点，[x,y]，是英雄实际位置
        :param pointList: 输入点列表 是一串点的位置
        :return: 返回最近点的序号
        '''
        print('closePointDetact point:{}'.format(point))
        assert (len(point) == 2)
        print(pointList)
        point = np.array(point).reshape(1, 2)
        pointList = np.array(pointList).reshape(-1, 2)
        assert (point.shape == (1, 2))
        assert (pointList.shape[1] == 2)
        a = pointList - point
        a = a * a
        a = a[:, 0] + a[:, 1]
        a = np.argmin(a)
        return a



    def elementExtract(self,elementName,oriPic):
        '''
        从图片中提取某些元素，如小地图，血条，蓝条等，具体数据在self.postionData
        :param elementName: 元素名称 具体看那个字典
        :param oriPic: 原始图片 格式cv2图片
        :return: 返回地图，格式cv2图片
        '''
        pass

    def loadPic(self,path= 'res/Screen01.png'):
        pic=cv2.imread(path)
        return pic

    def picDisplay(self,pic,saveName = ''):
        if np.max(pic) <= 1:
            pic = pic * 255
        cv2.imshow('pic',pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if saveName != '':
            cv2.imwrite('ans/'+saveName+'.png',pic)

    def smallMapExtract(self,oriPic):
        mapPic = oriPic[538:719,1100:1279]
        return mapPic

    def pointTransform(self,pointIn,map2all = False):
        '''
        :param pointIn: 输入坐标，【X，Y】
        :param map2all: 如果是小地图转通用坐标，该参数为True
        :return:返回坐标值列表，【y，x】
        '''
        pointIn = pointIn.copy()
        yOffset = self.postionData['MAP'][0]
        xOffset = self.postionData['MAP'][1]
        addRatio = -1
        if map2all:
            addRatio = 1
        pointIn[0] += addRatio * xOffset
        pointIn[1] += addRatio * yOffset
        return pointIn


    def postionInSmallMapExtract(self,mapPic):
        #input pic is 0 and 1 matric
        #输入是小地图那个白框的矩阵图像，所有值只有0和1
        if np.max(mapPic) > 1:
            print('图片数据大于1')
        if (mapPic == 0).all():
            print('图片全为0')
            return

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 定义结构元素
        mapPic = cv2.morphologyEx(mapPic, cv2.MORPH_OPEN, kernel)  # 开运算
        # self.picDisplay(mapPic,'map2')
        # exit()

        lieHe = np.sum(mapPic,axis = 0)#每列求和，最后是一行
        hangHe = np.sum(mapPic,axis = 1)#每行求和，最后是一列

        lieKuangXianPos = []
        hangKuangXianPos = []
        lieAreaList = []
        hangAreaList = []
        for i in range(len(lieHe)):
            if lieHe[i]> 6:
                lieKuangXianPos.append(i)
            elif lieHe[i]>0:
                lieAreaList.append(i)

        for i in range(len(hangHe)):
            if hangHe[i] > 6:
                hangKuangXianPos.append(i)
            elif hangHe[i]>0:
                hangAreaList.append(i)


        # print('行坐标：%s 列坐标：%s'%(hangKuangXianPos,lieKuangXianPos))
        # print('中心点坐标：%s'%([np.mean(hangKuangXianPos),np.mean(lieKuangXianPos)]))
        # print(lieAreaList)
        # print(hangAreaList)

        # 行坐标：[143, 144, 170, 171] 实际为竖直坐标
        # 列坐标：[89, 90, 137, 138] 实际为水平坐标
        # 中心点坐标：[157.0, 113.5]
        # 竖直坐标间距13.5 水平坐标间距24 半个矩形长度，到中心点距离


        #为了处理部分矩形边框超出小地图范围的情况
        centerPos = []
        centerPos.append(np.mean(lieAreaList))#中心点横坐标
        centerPos.append(np.mean(hangAreaList))#中心点纵坐标

        hangChangdu = len(hangKuangXianPos)
        lieChangdu = len(lieKuangXianPos)
        hangKuangXianPos = np.array(hangKuangXianPos).reshape(1,hangChangdu)
        lieKuangXianPos = np.array(lieKuangXianPos).reshape(1,lieChangdu)

        #通过聚类算法获取边框中线位置 此处为纵坐标获取
        zeros = np.zeros([1, hangChangdu])
        points = np.array([hangKuangXianPos, zeros]).T.reshape(hangChangdu,2)
        # print(points)
        # print(points.shape)
        ms = MeanShift(bandwidth=2)
        ms.fit(points)

        cluster_centers = ms.cluster_centers_
        print(cluster_centers)
        ys = []
        for i in cluster_centers:
            for j in i:
                if j!=0:
                    ys.append(j)

        #通过聚类算法获取边框中线位置 此处为横坐标获取
        zeros = np.zeros([1, lieChangdu])
        points = np.array([lieKuangXianPos, zeros]).T.reshape(lieChangdu,2)
        # print(points)
        # print(points.shape)
        ms = MeanShift(bandwidth=4)
        ms.fit(points)

        cluster_centers = ms.cluster_centers_
        # print(cluster_centers)
        xs = []
        for i in cluster_centers:
            for j in i:
                if j!=0:
                    xs.append(j)

        centerPoint = [0,0]

        if len(xs) == 2:
            centerPoint[0] = np.mean(xs)
        elif len(xs) == 1:
            if xs[0] > centerPos[0]:
                centerPoint[0] = xs[0] - 24
            else:
                centerPoint[0] = xs[0] + 24
        else:
            print('err 聚类获取点非1，2个 xs：%s'%(xs))

        if len(ys) == 2:
            centerPoint[1] = np.mean(ys)
        elif len(ys) == 1:
            if ys[0] > centerPos[1]:
                centerPoint[1] = ys[0] - 13.5
            else:
                centerPoint[1] = ys[0] + 13.5
        else:
            print('err 聚类获取点非1，2个 ys：%s'%(ys))

        # print('估计中心点：%s 精确中心点：%s'%(centerPos,centerPoint))
        return centerPoint

    def picSize(self,img):
        height = len(img)
        width = len(img[0])
        print('图片大小%dX%d' % (width, height))

    def skeletonGene(self,img):
        skeleton =morphology.skeletonize(img)
        return skeleton

    def postionExtract(self,pic = 0):
        '''
        封装提取位置
        :param pic: 全局图像
        :return: 位置
        '''
        if pic == 0:
            pic = self.currentPic
        pic = p.smallMapExtract(pic)
        print(np.max(pic),np.min(pic))

        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
        print(np.max(pic),np.min(pic))

        pic = np.uint8((pic > 254) * 1)
        centerPoint = p.postionInSmallMapExtract(pic)
        return centerPoint

    def determineAction(self,pic = 0):
        '''
        通过输入图片决定所需动作 局势检测等在此实现

        :param pic: 当前完整图片
        :return: 动作字典
        '''
        if pic == 0:
            pic = self.currentPic


        action = {
            'go':1
        }
        return action

    def paramExtract(self,pic = 0):
        '''
        通过游戏图像获取游戏动作执行过程中所需的参数
        :param pic:
        :return:动作等所需参数
        '''
        params = {}
        if pic == 0:
            pic = self.currentPic
        centerPoint = self.postionExtract()
        print('after extract:{}'.format(centerPoint))
        centerPoint = self.pointTransform(centerPoint,True)
        print('after Transform:{}'.format(centerPoint))
        print(centerPoint)
        closePointIndex = self.closePointDetact(centerPoint,self.bottomNodeList)
        print('最近点序号：{}'.format(closePointIndex))
        backIndex = closePointIndex - 1
        goIndex = closePointIndex + 1
        if backIndex < 0:
            backIndex = 0
        l = len(self.bottomNodeList)
        if goIndex > l:
            goIndex = l
        params['back'] = self.bottomNodeList[backIndex]
        params['go'] = self.bottomNodeList[goIndex]

        return params

    def actionExcute(self,action,params):
        '''
        执行程序发出的指令到游戏
        :param action:指令字典
        :return:无
        '''
        go = action['go']
        targetPostionName = ''
        if go == 1:
            targetPostionName = 'go'
        elif go == -1:
            targetPostionName = 'back'

        targetPostion = params.get(targetPostionName,None)
        if targetPostion is not None:
            self.operater.MoveToMapPostion(targetPostion)
            self.operater.sendCommand()

    def getPic(self,pic):
        '''
        获取图片的函数，图片从此开始处理
        :param pic:游戏全图
        :return:
        '''
        print(pic.shape)
        assert (pic.shape == (720,1280,3))
        same = (pic == self.currentPic).all()
        print('获取图片 重复判断结果：{}'.format(same))
        if same:
            return
        self.currentPic = pic
        action = self.determineAction()
        params = self.paramExtract()
        self.actionExcute(action,params)

    def mainLoop(self):
        while(True):
        #if True:
            pic = self.loadPic('dm/screen1/0.bmp')
            if pic is not None:
                self.getPic(pic)
            else:
                time.sleep(0.1)





if __name__ == "__main__":
    p = picProcesser()
    p.mainLoop()
    exit()
    print (p.nodesPostions.keys())
    pic = p.loadPic('res/Screen19.png')

    print(pic.shape)
    pic = p.smallMapExtract(pic)

    pic=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)

    pic = np.uint8((pic>254)*1)
    centerPoint = p.postionInSmallMapExtract(pic)


