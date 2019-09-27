import cv2
import numpy as np


def findPics(oriImg, targetImg, mask = None, threshold=0.8, delay=0.5, test=False):
	h, w = targetImg.shape[:2]  # rows->h, cols->w
	h2, w2 = oriImg.shape[:2]  # rows->h, cols->w
	res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)
	img = oriImg.copy()

	while(True):
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		print(max_val)

		horizen0 = np.max(0,max_loc[0]-w//2)
		horizen1 = np.min(w2,max_loc[0]+w//2)
		vertical0 = np.max(0,max_loc[1]-h//2)
		vertical1 = np.min(h2,max_loc[1]+w//2)

		res[horizen0:horizen1,vertical0,vertical1] = 0

		postions = []

		if max_val > threshold:
			left_top = max_loc  # 左上角
			right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
			if test:
				cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
			postions.append([left_top, right_bottom])
		else:
			break
	if test:
		cv2.imwrite('result.png', img)

	return postions


def findPic(oriImg, targetImg, mask=None, threshold=0.8, test=False):
	h, w = targetImg.shape[:2]  # rows->h, cols->w
	res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	maxValue = np.max(res)
	print(maxValue)
	if maxValue > threshold or True:
		left_top = max_loc  # 左上角
		right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
		if test:
			# print(maxValue)
			img = oriImg.copy()
			cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置
			cv2.imwrite('result.png', img)
			cv2.imwrite('mask2.png', mask)

		return [left_top, right_bottom]


if __name__ == "__main__":
	target = cv2.imread('target.png')
	mask = cv2.imread('mask3.png')
	img0 = cv2.imread(r'E:\develop\autoLOLres\ans\screen779.bmp')


	findPics(img0, target, mask, test=True)


