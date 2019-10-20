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

def HpPicExtract(oriPic):
	'''
	从图片中提取血条
	:param oriPic: 原始图片 格式cv2图片
	:return: 返回血条，格式cv2图片
	'''
	targetArea = [454,686,730,697]
	pic = oriPic[targetArea[1]:targetArea[3], targetArea[0]:targetArea[2]].copy()
	return pic

def findPic(oriImg, targetImg, threshold=0.8, delay=0.5, test=False):
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

def getCharImgs(self, pic):
	'''
	extrat char img from a hp or mp img
	:param pic:the hp or mp img
	:param add2List:
	:return:
	'''
	leftTop, rightBottom = findPic(pic, self.HPxieImg)

	# 将血条分为左右两侧
	zuoPic = pic[:, 0:leftTop[0] - 1].copy()
	youPic = pic[:, rightBottom[0] + 1:].copy()

	# 用于判断是否该像素列为空
	zuoLieSum = np.sum(zuoPic, axis=0)
	youLieSum = np.sum(youPic, axis=0)

	zuoLieSum = clearSmallConnectPoint(self,zuoLieSum)
	youLieSum = clearSmallConnectPoint(self,youLieSum)

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


def hpExtract2(self,pic = None):
	'''
	提取HP的百分比值，来源为self.currentPic
	返回值为0-1浮点数
	识别失败将返回None
	'''
	if pic is None:
		pic = self.currentPic
	pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
	pic = np.uint8(pic > 150)

	hpImg = HPExtract(pic)
	zuoImgs, youImgs = getCharImgs(self,hpImg)

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

	print('zuo:{} you:{} zuoNums:{} youNums:{}'.format(zuo, you, zuoNums, youNums))

	percent = -1
	try:
		percent = zuo / you
	except:
		pass
	print('the percent of HP:{} zuo:{} you:{}'.format(percent,zuo,you))
	return percent

def hpExtract(self,pic = None):
	if pic is None:
		pic = self.currentPic.copy()
	imgBGR = HpPicExtract(pic)
	b = imgBGR[:, :, 0]
	g = imgBGR[:, :, 1]
	r = imgBGR[:, :, 2]
	greenbgr = np.where(g-r>30) and np.where(g-b>30)
	b[:, :] = 0
	b[greenbgr] = 1
	outPic = np.zeros_like(b)
	b[greenbgr] = 255
	green = np.sum(b, axis=0)
	green = (green > 0)
	hp = np.sum(green)
	hp = hp / green.shape[0]
	print('the percent of HP:{}'.format(hp))
	return hp

class p:
	def __init__(self):
		self.HPxieImg = cv2.imread(r'E:\develop\autoLOL\resource\xie.png')
		self.HPxieImg = cv2.cvtColor(self.HPxieImg, cv2.COLOR_BGR2GRAY)

if __name__ == '__main__':
	i = 1
	while(True):
		imgBGR = cv2.imread(r'E:\develop\autoLOL\ans\game0\{}.png'.format(i))
		imgBGR = HpPicExtract(imgBGR)
		hp = hpExtract(None,imgBGR)
		print(i,hp)
		i += 1