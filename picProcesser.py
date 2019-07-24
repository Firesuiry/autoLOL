import numpy as np
import cv2
from skimage import morphology
from sklearn.cluster import MeanShift

class picProcesser():
    def __init__(self):
        pass

    def loadPic(self,path= 'res/Screen01.png'):
        pic=cv2.imread(path)
        return pic

    def picDisplay(self,pic,saveName = ''):
        cv2.imshow('pic',pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if saveName != '':
            cv2.imwrite('ans/'+saveName+'.png',pic)

    def smallMapExtract(self,oriPic):
        print(oriPic.shape)
        mapPic = oriPic[538:719,1100:1279]
        print(mapPic.size)
        return mapPic

    def postionInSmallMapExtract(self,mapPic):
        #input pic is 0 and 1 matric
        #输入是小地图那个白框的矩阵图像，所有值只有0和1
        if np.max(mapPic) > 1:
            print('图片数据大于1')

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
        ms = MeanShift(bandwidth=2)
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
            print('err 聚类获取点非1，2个 xs：%s'(xs))

        if len(ys) == 2:
            centerPoint[1] = np.mean(ys)
        elif len(ys) == 1:
            if ys[0] > centerPos[1]:
                centerPoint[1] = ys[0] - 13.5
            else:
                centerPoint[1] = ys[0] + 13.5
        else:
            print('err 聚类获取点非1，2个 ys：%s'(ys))

        # print('估计中心点：%s 精确中心点：%s'%(centerPos,centerPoint))
        return centerPoint






    def picSize(self,img):
        height = len(img)
        width = len(img[0])
        print('图片大小%dX%d' % (width, height))

    def skeletonGene(self,img):
        skeleton =morphology.skeletonize(img)
        return skeleton

if __name__ == "__main__":
    p = picProcesser()
    pic = p.loadPic('res/Screen19.png')
    pic = p.smallMapExtract(pic)

    pic=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)

    pic = np.uint8((pic>254)*1)
    centerPoint = p.postionInSmallMapExtract(pic)

