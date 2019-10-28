import numpy as np
import cv2

def HpPicExtract(oriPic):
	'''
	从图片中提取血条
	:param oriPic: 原始图片 格式cv2图片
	:return: 返回血条，格式cv2图片
	'''
	targetArea = [454,686,730,697]
	pic = oriPic[targetArea[1]:targetArea[3], targetArea[0]:targetArea[2]].copy()
	return pic

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

if __name__ == '__main__':
	i = 1
	while(True):
		imgBGR = cv2.imread(r'E:\develop\autoLOL\ans\game0\{}.png'.format(i))
		imgBGR = HpPicExtract(imgBGR)
		hp = hpExtract(None,imgBGR)
		print(i,hp)
		i += 1