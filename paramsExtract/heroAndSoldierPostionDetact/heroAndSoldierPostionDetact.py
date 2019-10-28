import cv2
import numpy as np



def findPics(oriImg, targetImg, mask = None, threshold=0.8, delay=0.5, test=False,color = [255,0,0] , maxThreshold = 1.1):
	print(oriImg.shape)
	h, w = targetImg.shape[:2]  # rows->h, cols->w
	h2, w2 = oriImg.shape[:2]  # rows->h, cols->w
	res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)
	img = oriImg.copy()
	postions = []
	while(True):
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		#找出来以后 loc的左边顺序是反的

		print(max_val,res[max_loc[1],max_loc[0]],np.max(res))
		print('max_loc:{} max_val:{}'.format(max_loc,max_val))

		horizen0 = np.max([0,max_loc[1]-h//2])
		horizen1 = np.min([h2,max_loc[1]+h//2])
		vertical0 = np.max([0,max_loc[0]-w//2])
		vertical1 = np.min([w2,max_loc[0]+w//2])



		if max_val > threshold and max_val < maxThreshold:
			left_top = max_loc  # 左上角
			right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
			if test:
				cv2.rectangle(img, left_top, right_bottom, color, 1)  # 画出矩形位置
			postions.append([left_top, right_bottom])
		elif max_val <= threshold:
			break
		res[horizen0:horizen1,vertical0:vertical1] = 0
	if test:
		cv2.imwrite('result.png', img)

	return postions

def gezi(img,space):
	w,h = img.shape[:2]
	for i in range(h // space):
		cv2.line(img,(space*(i+1),0),(space*(i+1),w-1),(255,255,255))

	for i in range(w // space):
		cv2.line(img,(0,space*(i+1)),(h-1,space*(i+1)),(255,255,255))
	return img


if __name__ == "__main__":

	target = cv2.imread('target.png')
	mask = cv2.imread('mask3.png')
	img0 = cv2.imread(r'D:\develop\autoLOLres\ans1\screen185.bm.jpg')

	target2 = cv2.imread('xiaobingHP.png')
	mask2 = cv2.imread('xiaobingHP_mask_l.png')



	findPics(img0, target, mask, test=True,threshold = 0.99)

	img0[np.where(np.sum(img0,axis=2) < 90)] = [0,0,0]
	target2[np.where(np.sum(target2,axis=2) < 90)] = [0,0,0]
	# findPics(img0, target2, mask2, test=True,threshold= 0.9,color=[255,255,255],maxThreshold= 0.99)


	#
	# cv2.imwrite('xiaobingHP2.png', target2[:,:10])
	# cv2.imwrite('xiaobingHP3.png', target2[:,-10:])
	#
	# cv2.imwrite('xiaobingHP_mask2.png', mask2[:,:10])
	# cv2.imwrite('xiaobingHP_mask3.png', mask2[:,-10:])
	lineImg = img0.copy()
	cv2.imwrite('line.png', gezi(lineImg,20))