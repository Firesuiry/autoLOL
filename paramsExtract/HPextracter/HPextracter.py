import numpy as np
import cv2

def clearSmallConnectPoint(self, sumList):
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


def getCharImgs(self, pic):
	'''
	extrat char img from a hp or mp img
	:param pic:the hp or mp img
	:param add2List:
	:return:
	'''
	leftTop, rightBottom = self.findPic(pic, self.HPxieImg)

	# 将血条分为左右两侧
	zuoPic = pic[:, 0:leftTop[0] - 1].copy()
	youPic = pic[:, rightBottom[0] + 1:].copy()

	# 用于判断是否该像素列为空
	zuoLieSum = np.sum(zuoPic, axis=0)
	youLieSum = np.sum(youPic, axis=0)

	zuoLieSum = clearSmallConnectPoint(self,zuoLieSum)
	youLieSum = clearSmallConnectPoint(self,youLieSum)

	# print(zuoPic.shape,zuoLieSum.shape)
	#     print(youLieSum)
	#plt.imshow(zuoPic)
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

	return [zuoCharImgs, youCharImgs]

def hpExtract(self):
	'''
	提取HP的百分比值，来源为self.currentPic
	返回值为0-1浮点数
	识别失败将返回None
	'''
	pic = cv2.cvtColor(self.currentPic, cv2.COLOR_BGR2GRAY)
	pic = np.uint8(pic > 150)

	hpImg = self.elementExtract('HP', pic)
	zuoImgs, youImgs = getCharImgs(self,hpImg)
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

	#print('zuo:{} you:{} zuoNums:{} youNums:{}'.format(zuo, you, zuoNums, youNums))

	percent = -1
	try:
		percent = zuo / you
	except:
		pass
	print('the percent of HP:{}'.format(percent))
	return percent