import cv2,time,os,sys
PATH = os.path.split(__file__)[0] + '/'


class Main:
	def __init__(self,dm):
		self.视角锁定图片 = cv2.imread(PATH + r"camera.png")
		self.dm = dm

	def INIT(self):
		if self.窗口未锁定():
			self.锁定窗口()

		if self.窗口未锁定():
			self.锁定窗口()

		if self.窗口未锁定():
			print('窗口锁不了。。请检查原因')
			exit()

	def 锁定窗口(self):
		# time.sleep(1)
		time.sleep(0.1)
		dm_ret = self.dm.MoveTo(100,100)
		time.sleep(0.1)
		dm_ret = self.dm.LeftClick()
		time.sleep(0.5)
		# dm_ret = self.dm.KeyPressChar('Y')
		self.dm.KeyPressChar('Y')
		time.sleep(0.3)

	def 窗口未锁定(self):
		pic = self.dm.get_game_img()
		res = cv2.matchTemplate(pic, self.视角锁定图片, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		return max_val > 0.99




if __name__ == '__main__':
	pass
