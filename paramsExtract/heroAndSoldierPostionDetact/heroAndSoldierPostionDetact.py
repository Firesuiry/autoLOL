import cv2
import numpy as np


def findPics(oriImg, targetImg, mask = None, threshold=0.8, delay=0.5, test=False):
	h, w = targetImg.shape[:2]  # rows->h, cols->w
	res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)
	img = oriImg.copy()

	while(True):
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		print(max_val)

		horizen = range(res.shape[0])
		vertical = range(res.shape[1])

		horizen = np.abs(horizen - left_top[0]) < w // 2
		vertical = np.abs(vertical - left_top[1]) < h // 2


		res[horizen,vertical] = 0

		if max_val > threshold:
			left_top = max_loc  # 左上角
			right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
			if test:
				# print(maxValue)
				cv2.rectangle(img, left_top, right_bottom, 255, 1)  # 画出矩形位置

		else:
			break
	if test:
		cv2.imwrite('result.png', img)

	return [left_top, right_bottom]


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


	findPic(img0, target, None, test=True)

	findPic(img0, target, mask, test=True)
