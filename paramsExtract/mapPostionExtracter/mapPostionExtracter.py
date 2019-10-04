import numpy as np
import cv2
from sklearn.cluster import MeanShift

def postionInSmallMapExtract(self, mapPic):
	# input pic is 0 and 1 matric
	# 输入是小地图那个白框的矩阵图像，所有值只有0和1
	if np.max(mapPic) > 1:
		print('图片数据大于1')
	if (mapPic == 0).all():
		print('图片全为0')
		return

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 定义结构元素
	mapPic = cv2.morphologyEx(mapPic, cv2.MORPH_OPEN, kernel)  # 开运算
	# self.picDisplay(mapPic,'map2')
	# exit()

	lieHe = np.sum(mapPic, axis=0)  # 每列求和，最后是一行
	hangHe = np.sum(mapPic, axis=1)  # 每行求和，最后是一列

	lieKuangXianPos = []
	hangKuangXianPos = []
	lieAreaList = []
	hangAreaList = []
	for i in range(len(lieHe)):
		if lieHe[i] > 6:
			lieKuangXianPos.append(i)
		elif lieHe[i] > 0:
			lieAreaList.append(i)

	for i in range(len(hangHe)):
		if hangHe[i] > 6:
			hangKuangXianPos.append(i)
		elif hangHe[i] > 0:
			hangAreaList.append(i)

	# print('行坐标：%s 列坐标：%s'%(hangKuangXianPos,lieKuangXianPos))
	# print('中心点坐标：%s'%([np.mean(hangKuangXianPos),np.mean(lieKuangXianPos)]))
	# print(lieAreaList)
	# print(hangAreaList)

	# 行坐标：[143, 144, 170, 171] 实际为竖直坐标
	# 列坐标：[89, 90, 137, 138] 实际为水平坐标
	# 中心点坐标：[157.0, 113.5]
	# 竖直坐标间距13.5 水平坐标间距24 半个矩形长度，到中心点距离

	# 为了处理部分矩形边框超出小地图范围的情况
	centerPos = []
	centerPos.append(np.mean(lieAreaList))  # 中心点横坐标
	centerPos.append(np.mean(hangAreaList))  # 中心点纵坐标

	hangChangdu = len(hangKuangXianPos)
	lieChangdu = len(lieKuangXianPos)
	hangKuangXianPos = np.array(hangKuangXianPos).reshape(1, hangChangdu)
	lieKuangXianPos = np.array(lieKuangXianPos).reshape(1, lieChangdu)

	# 通过聚类算法获取边框中线位置 此处为纵坐标获取
	zeros = np.zeros([1, hangChangdu])
	points = np.array([hangKuangXianPos, zeros]).T.reshape(hangChangdu, 2)
	# print(points)
	# print(points.shape)
	ms = MeanShift(bandwidth=2)
	ms.fit(points)

	cluster_centers = ms.cluster_centers_
	print(cluster_centers)
	ys = []
	for i in cluster_centers:
		for j in i:
			if j != 0:
				ys.append(j)

	# 通过聚类算法获取边框中线位置 此处为横坐标获取
	zeros = np.zeros([1, lieChangdu])
	points = np.array([lieKuangXianPos, zeros]).T.reshape(lieChangdu, 2)
	# print(points)
	# print(points.shape)
	ms = MeanShift(bandwidth=4)
	ms.fit(points)

	cluster_centers = ms.cluster_centers_
	# print(cluster_centers)
	xs = []
	for i in cluster_centers:
		for j in i:
			if j != 0:
				xs.append(j)

	centerPoint = [0, 0]

	if len(xs) == 2:
		centerPoint[0] = np.mean(xs)
	elif len(xs) == 1:
		if xs[0] > centerPos[0]:
			centerPoint[0] = xs[0] - 24
		else:
			centerPoint[0] = xs[0] + 24
	else:
		print('err 聚类获取点非1，2个 xs：%s' % (xs))

	if len(ys) == 2:
		centerPoint[1] = np.mean(ys)
	elif len(ys) == 1:
		if ys[0] > centerPos[1]:
			centerPoint[1] = ys[0] - 13.5
		else:
			centerPoint[1] = ys[0] + 13.5
	else:
		print('err 聚类获取点非1，2个 ys：%s' % (ys))

	# print('估计中心点：%s 精确中心点：%s'%(centerPos,centerPoint))
	return centerPoint


def closePointDetact(self, point, pointList):
	'''
	:param point: 输入点，[x,y]，是英雄实际位置
	:param pointList: 输入点列表 是一串点的位置
	:return: 返回最近点的序号
	'''
	assert (len(point) == 2)
	point = np.array(point).reshape(1, 2)
	pointList = np.array(pointList).reshape(-1, 2)
	assert (point.shape == (1, 2))
	assert (pointList.shape[1] == 2)
	a = pointList - point
	a = a * a
	a = a[:, 0] + a[:, 1]
	a = np.argmin(a)
	return a

def postionExtract(self):
	'''
	封装提取位置
	:param pic: 全局图像
	:return: 位置
	'''

	pic = self.currentPic
	pic = self.elementExtract('MAP', pic)

	pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

	pic = np.uint8((pic > 254) * 1)
	centerPoint = postionInSmallMapExtract(self,pic)
	return centerPoint


def centerParaExtract(self):
	centerPoint = postionExtract(self)
	#print('after extract:{}'.format(centerPoint))
	centerPoint = self.pointTransform(centerPoint, True)
	#print('after Transform:{}'.format(centerPoint))
	#print(centerPoint)
	closePointIndex = closePointDetact(self,centerPoint, self.bottomNodeList)
	print('最近点序号：{}'.format(closePointIndex))
	backIndex = closePointIndex - 1
	goIndex = closePointIndex + 1
	if backIndex < 0:
		backIndex = 0
	l = len(self.bottomNodeList)
	if goIndex > l:
		goIndex = l
	re1 = self.bottomNodeList[backIndex].tolist()
	re2 = centerPoint
	re3 = self.bottomNodeList[goIndex].tolist()
	return re1,re2,re3