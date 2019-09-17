import numpy as np
import cv2
from skimage import morphology
from sklearn.cluster import MeanShift
from operater import operater
import time
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf



class picProcesser():
	def __init__(self):
		self.operater = operater()
		self.ai = smartAI()
		self.dataInit()

	def dataInit(self):
		'''
		init the data which is need in the processer
		:return:None
		'''
		self.currentPic = None
		#x0,y0,x1,y1
		self.postionData = {
			'HP':[454,686,730,697],
			'MP':[454,699,730,710],
			'MONEY':[753,694,730,714],
			'MAP':[1100,538,1279,719]
		}
        #节点名称介绍
		'''
		首位 L左下边 R右上边
		次位 Base基地（结束） T上 M中 B下
		再次 Node 召唤节点（结束） T塔 R河道边
		再次 1高地塔（结束） 2二塔（结束） 3边塔（结束） 0门牙塔
		再次 0左门牙塔（结束） 1右门牙塔（结束）
		'''
		self.nodesPostions = {
			'LSpring':[1105,707],
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
		self.bottomNodeKeys = ['LSpring','LBase', 'LBNode', 'LBT1', 'LBT2', 'LBT3','LBR','RBR', 'RBT3', 'RBT2', 'RBT1', 'RBNode', 'RT01', 'RT00', 'RBase']
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
		#HP提取时用的中间的斜线
		self.HPxieImg = cv2.imread('resource/xie.png')
		self.HPxieImg = cv2.cvtColor(self.HPxieImg, cv2.COLOR_BGR2GRAY)

	def posCaculate(self,x,y,bottom = False,top = False,middle = False):
		if not (bottom or top or middle):
			bottom = True

		if bottom:
			pos = [x,y]

	def findPic(self,oriImg, targetImg, threshold=0.8, delay=0.5, test=False):
		point = [0, 0]
		h, w = targetImg.shape[:2]  # rows->h, cols->w
		res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		maxValue = np.max(res)
		# print(maxValue)
		if maxValue > threshold or True:
			left_top = max_loc  # 左上角
			right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
			if test:
				# print(maxValue)
				img = oriImg.copy()
				cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
				cv2.imwrite('result.png', img)

			return [left_top, right_bottom]

	def getCharImgs(self,pic):
		'''
		extrat char img from a hp or mp img
		:param pic:the hp or mp img
		:param add2List:
		:return:
		'''
		leftTop,rightBottom = self.findPic(pic,self.HPxieImg)

		# 将血条分为左右两侧
		zuoPic = pic[:, 0:leftTop[0] - 1].copy()
		youPic = pic[:, rightBottom[0] + 1:].copy()

		# 用于判断是否该像素列为空
		zuoLieSum = np.sum(zuoPic, axis=0)
		youLieSum = np.sum(youPic, axis=0)

		zuoLieSum = self.clearSmallConnectPoint(zuoLieSum)
		youLieSum = self.clearSmallConnectPoint(youLieSum)

		# print(zuoPic.shape,zuoLieSum.shape)
		#     print(youLieSum)
		plt.imshow(zuoPic)
		#     plt.show()
		# 开始处理右侧数字
		blankLie = 0
		index = 0
		youCharImgs = []
		charStart = -1
		while (blankLie < 8 and index < len(youLieSum)):
			isBlank = youLieSum[index]  # 0表示此处为空
			# print(index,isBlank)
			if isBlank == 0:
				blankLie += 1
				if charStart != -1:
					charEnd = index
					if charEnd - charStart > 3:
						if charEnd - charStart < 6:
							charEnd = charStart + 6
						youCharImgs.append(youPic[:, charStart:charEnd])
					# print('char start and end:',charStart,charEnd)
					charStart = -1
			else:
				if charStart == -1:
					charStart = index
					blankLie = 0
			index += 1

		# print('开始处理左侧数字')
		# 开始处理左侧数字
		blankLie = 0
		index = len(zuoLieSum) - 1
		zuoCharImgs = []
		charEnd = -1  # 因为是从右往左看,所以是以end为标志
		while (blankLie < 8 and index > 0):
			isBlank = zuoLieSum[index]
			# print(index,isBlank)
			if isBlank == 0:
				blankLie += 1
				if charEnd != -1:
					charStart = index + 1
					if charEnd - charStart > 3:
						if charEnd - charStart < 6:
							charEnd = charStart + 6
						zuoCharImgs.append(zuoPic[:, charStart:charEnd])
					# print('char start and end:',charStart,charEnd)
					charEnd = -1
			else:
				if charEnd == -1:
					charEnd = index + 1
					blankLie = 0
			index -= 1

		

		return [zuoCharImgs,youCharImgs]

	def clearSmallConnectPoint(self,sumList):
		# 清理在列和表中出现的一些字符间不正确链接,用于HP提取
		# 思路是清理长段落都有值的 值为255的段落
		connectList = []  # 检测每个列左侧有多少个已经非空白的列
		sumList = np.array(sumList)
		notBlankLie = 0
		for i in range(len(sumList)):
			connectList.append(notBlankLie)
			if sumList[i] == 0:
				notBlankLie = 0
			else:
				notBlankLie += 1
		connectList = np.array(connectList)

		assert (len(sumList) == len(connectList))

		clearBools = 1 - (connectList > 4) * (sumList < 256)
		sumList = sumList * clearBools

		return sumList


	def closePointDetact(self,point,pointList):
		'''
		:param point: 输入点，[x,y]，是英雄实际位置
		:param pointList: 输入点列表 是一串点的位置
		:return: 返回最近点的序号
		'''
		#point1 = point.copy()
		#point[0] = point1[1]
		#point[1] = point1[0]
		#print('closePointDetact point:{}'.format(point))
		assert (len(point) == 2)
		#print(pointList)
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
		print ('elementExtract elment:{}'.format(elementName))
		targetArea = self.postionData.get(elementName,None)
		assert targetArea is not None
		print (targetArea)
		pic = oriPic[targetArea[1]:targetArea[3], targetArea[0]:targetArea[2]]
		return pic

	def loadPic(self,path= 'res/Screen01.png'):
		pic=cv2.imread(path)
		return pic

	def picDisplay(self,pic,saveName = '',PIL = False,noDis = False):
		if np.max(pic) <= 1:
			pic = pic * 255
		if not noDis:
			if not PIL:
				cv2.imshow('pic',pic)
				cv2.waitKey(0)
				cv2.destroyAllWindows()
			else:
				plt.figure(saveName)
				plt.imshow(pic)
				plt.show()
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
		pointIn[0] += addRatio * yOffset
		pointIn[1] += addRatio * xOffset
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

	def determineAction(self,params = {}):
		'''
		通过输入图片决定所需动作 局势检测等在此实现

		:param pic: 当前完整图片
		:return: 动作字典
		'''

		pic = self.currentPic

		go = 1
		HPpercent = params.get('HP',-1)
		print('当前HP:{}'.format(HPpercent))
		if HPpercent == -1:
			pass
		elif HPpercent < 0.95:
			print('撤退')
			go = -1

		action = {
			'go':go
		}
		return action

	def centerParaExtract(self):
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
		return self.bottomNodeList[backIndex],centerPoint,self.bottomNodeList[goIndex]

	def paramExtract(self,pic = 0):
		'''
		通过游戏图像获取游戏动作执行过程中所需的参数
		:param pic:
		:return:动作等所需参数
		'''
		params = {}
		pic = self.currentPic
		params['back'],params['postion'],params['go'] = self.centerParaExtract()
		params['HP'] = self.hpExtract()
		return params

	def hpExtract(self):
		'''
		提取HP的百分比值，来源为self.currentPic
		返回值为0-1浮点数
		识别失败将返回None
		'''
		pic = cv2.cvtColor(self.currentPic, cv2.COLOR_BGR2GRAY)
		pic = np.uint8(pic>150)

		hpImg = self.elementExtract('HP',pic)
		zuoImgs,youImgs = self.getCharImgs(hpImg)
		for img in zuoImgs:
			print(img.shape)
		zuoNums = self.ai.hpDightRecognizate(zuoImgs)
		youNums = self.ai.hpDightRecognizate(youImgs)
		zuo = 0
		you = 0

		for num in zuoNums[::-1]:
			zuo *= 10
			zuo += num

		for num in youNums:
			you *= 10
			you += num

		print('zuo:{} you:{} zuoNums:{} youNums:{}'.format(zuo,you,zuoNums,youNums))

		percent = -1
		try:
			percent = zuo / you
		except:
			pass
		print('the percent of HP:{}'.format(percent))
		return percent






	def colorDelate(self,pic,green = True,blue = True):
		b = pic[:,:,0]
		g = pic[:,:,1]
		r = pic[:,:,2]


		if green:
			clearBool = 1 - np.uint8(g - r > 40) * np.uint8(g - b > 40)
			pic[:, :, 0] *= clearBool
			pic[:, :, 1] *= clearBool
			pic[:, :, 2] *= clearBool

		if blue:
			clearBool = 1 - np.uint8(b - r > 30) * np.uint8(b - g > 30)
			pic[:, :, 0] *= clearBool
			pic[:, :, 1] *= clearBool
			pic[:, :, 2] *= clearBool



		return pic


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
			self.operater.MoveToMapPostion(targetPostion,targetPostionName == 'go')
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
		params = self.paramExtract()
		action = self.determineAction(params)
		self.actionExcute(action,params)

	def mainLoop(self):
		while(True):
		#if True:
			pic = self.loadPic('dm/screen1/0.bmp')
			if pic is not None:
				self.getPic(pic)
			else:
				time.sleep(0.1)


class smartAI():
	def __init__(self):
		self.HPdigitModel_ = None
		self.HPdigits = []

		x = []
		i = 0
		while True:
			pic = cv2.imread(r'jupyter/shuzi/{}.png'.format(i))
			if pic is None:
				break
			pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
			x.append(pic)
			i += 1
		self.x = np.array(x)
		print(self.x.shape)



	def HPdigitModel(self):
		if self.HPdigitModel_ is not None:
			return self.HPdigitModel_
		else:
			self.HPdigitModel_ = tf.keras.models.load_model(r'model/HP_Num_Recognition_model.h5')
			return self.HPdigitModel_

	def hpDightRecognizate(self,charImgs):
		print(type(charImgs),len(charImgs))

		for img in charImgs:
			if img.shape == (11,6):
				continue

			plt.figure('')
			plt.imshow(img)
			plt.show()

		
		charImgs = np.uint8(np.array(charImgs))

		print('there are {} imgs to recognize || shape is {}'.format(len(charImgs),charImgs.shape))
		ansLs = []
		for i in range(len(charImgs)):
			
			targetImg = charImgs[i] * 255

			predictions = self.HPdigitModel().predict(targetImg.reshape(1,11,6))
			ans = np.argmax(predictions)
			#maxValue = np.max(predictions)
			#print(ans,maxValue)
			#for x in self.x:
			#	if (x == targetImg).all():
			#		print('find x is the same ')
			#		break
			#plt.figure('')
			#plt.imshow(targetImg)
			#plt.show()
			ansLs.append(ans)

		return ansLs












def HPextract():
	print(p.nodesPostions.keys())
	i = 1
	while(True):
		pic = p.loadPic(r'E:\develop\autoLOLres\ans\screen{}.bmp'.format(i))
		assert pic is not None
		pic = p.colorDelate(pic)
		pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
		pic = np.uint8(pic>150)
		pic = p.elementExtract('HP',pic)
		p.picDisplay(pic,'HP{}'.format(i),True,True)
		i += 1


if __name__ == "__main__":
	 p = picProcesser()
	 p.mainLoop()
	 exit()
	#AI = smartAI()
	#p = picProcesser()
	#i = 1000
	#pic = p.loadPic(r'E:\develop\autoLOLres\ans\screen{}.bmp'.format(i))
	#cv2.imwrite('logOut/0.png',pic)
	#p.currentPic = pic
	#p.hpExtract()


