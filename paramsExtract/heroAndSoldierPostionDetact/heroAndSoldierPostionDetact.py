import cv2
import numpy as np

class targetDetacter():
	def __init__(self):
		self.hero_target = cv2.imread('target.png')
		self.hero_mask = cv2.imread('mask3.png')

		self.enemy_soldier_target_full = cv2.imread('xiaobingHP.png')
		self.ally_soldier_target_full = cv2.imread('soldier_hp_self.png')
		self.ally_soldier_target_full = self.colorClear(self.ally_soldier_target_full)
		self.enemy_soldier_target_full = self.colorClear(self.enemy_soldier_target_full)
		self.soldier_mask_full = cv2.imread('xiaobingHP_mask_l.png')

	@staticmethod
	def colorClear(img):
		img[np.where(np.sum(img, axis=2) < 120)] = [0, 0, 0]
		img[np.where((np.max(img,axis= 2) - np.min(img,axis=2) < 25 )&( np.sum(img, axis=2) < 300))] = [0,0,0]
		return img


	@staticmethod
	def colorCheck(img,postions,blue = False,red = False):
		new_postions = []
		for pos in postions:
			x = pos[0] + 1
			y = pos[1] + 1

			color = img[pos[1]+1:pos[1] + 4,pos[0]+1,:]
			cv2.imwrite('f.png',color)
			print(img.shape)
			print(color.shape)
			b = color[:,0]
			g = color[:,1]
			r = color[:,2]
			right_bool = False
			# print('pos:',pos)
			# print('color:',color)
			# if blue:
			# 	right_bool =


			if right_bool:
				new_postions.append(pos)
		return new_postions


	def getTargetPostions(self,img):
		dic = {}
		hero_postions = self.findPics(img, self.hero_target, self.hero_mask, test='hero',threshold = 0.96,color=[0,0,255])

		img0 = img.copy()
		img0 = self.colorClear(img0)
		enemy_soldier_postions = self.findPics(img0, self.enemy_soldier_target_full, self.soldier_mask_full, test='enemy_soldier',threshold= 0.85,color=[255,255,255],maxThreshold= 0.999)
		ally_soldier_postions = self.findPics(img0, self.ally_soldier_target_full, self.soldier_mask_full, test='ally_soldier',threshold= 0.85,color=[255,255,255],maxThreshold= 0.999)

		new_ally_soldier_postions = []
		new_enemy_soldier_postions = []
		self.colorCheck(img0,ally_soldier_postions)


		dic['hero'] = hero_postions
		dic['enemy_soldier'] = enemy_soldier_postions
		dic['ally_soldier'] = ally_soldier_postions

		return dic

	@staticmethod
	def findPics(oriImg, targetImg, mask = None, threshold=0.8, test='',color = [255,0,0] , maxThreshold = 1.1):
		print(oriImg.shape)
		h, w = targetImg.shape[:2]  # rows->h, cols->w
		h2, w2 = oriImg.shape[:2]  # rows->h, cols->w
		res = cv2.matchTemplate(oriImg, targetImg, cv2.TM_CCORR_NORMED, mask=mask)
		img = oriImg.copy()
		# img = oriImg
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
				if test is not '':
					cv2.rectangle(img, left_top, right_bottom, color, 1)  # 画出矩形位置
				postions.append(left_top)
			elif max_val <= threshold:
				break
			res[horizen0:horizen1,vertical0:vertical1] = 0
		if test is not '':
			cv2.imwrite('result{}.png'.format(test), img)

		return np.array(postions)


	@staticmethod
	def gezi(img,space):
		w,h = img.shape[:2]
		for i in range(h // space):
			cv2.line(img,(space*(i+1),0),(space*(i+1),w-1),(255,255,255))

		for i in range(w // space):
			cv2.line(img,(0,space*(i+1)),(h-1,space*(i+1)),(255,255,255))
		return img

hero_soldier_detacter = targetDetacter()

if __name__ == '__main__':
	# img0 = cv2.imread(r'D:\develop\autoLOLres\ans1\screen485.bm.jpg')
	img0 = cv2.imread(r'oriImg.jpg')
	hero_soldier_detacter.getTargetPostions(img0)
