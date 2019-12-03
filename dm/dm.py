# -*- coding: utf-8 -*-
import DmCommucation as dc
import time
import os, json
import cv2
import win32com.client
import sys
from dm_setting import *
import numpy as np
import multiprocessing as mp

PATH = os.path.abspath(__file__)[:-5]
print('当前文件执行目录：', PATH)


class dmBase():
	def __init__(self):
		self.id = 0

	def getCommand(self):
		f_path = r'E:\develop\autoLOL\dm\data\{}.txt'.format(self.id)
		command = ''
		if os.path.exists(f_path):
			with open(f_path) as f:
				command = f.read()
		# print(command)
		return command


class dmOperater(dc.DmCommucation):
	def __init__(self, id, hwnd, manager):
		self.id = id
		self.hwnd = hwnd
		self.manager = manager
		print('dmOperater启动，id：{} hwnd:{}'.format(id, hwnd))
		self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
		dm_ret = self.dm.SetShowErrorMsg(0)
		dm_ret = self.dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
		print('窗口绑定结果：%s' % dm_ret)
		if dm_ret == 0:
			return
		self.dm.MoveWindow(hwnd, 1, 1)
		self.dm.LockInput(1)
		if not os.path.exists('screen' + str(self.id)):
			os.makedirs('screen' + str(self.id))
		err_time = 0
		while True:
			try:
				self.start()
				break
			except Exception as e:
				err_time += 1
				print('发生错误：{} 当前出错次数：{}'.format(e,err_time))
				if err_time > 10:
					print('出错过多，退出当前进程')
					return
				time.sleep(2)

	def capture(self):
		dm_ret = self.dm.Capture(0, 0, 2000, 2000, "screen%s/0.bmp" % self.id)
		print('截图结果：{}'.format(dm_ret))

	def __getattr__(self, item):
		def dock(*args, **kwargs):
			if self.bind_ret == "失败": return "大漠未绑定窗口"
			return getattr(self.dm, item)(*args, **kwargs)

		return dock if item not in self.__dict__ else getattr(self, item)


class dm_hall_operater():
	def __init__(self, id, hwnd, manager, save_img=True):
		self.id = id
		self.hwnd = hwnd
		self.manager = manager
		self.save_img = save_img
		self.start_success = False
		if self.save_img:
			self.img_index = 1

		print('dm_hall_operater 启动，id：{} hwnd:{}'.format(id, hwnd))
		self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
		dm_ret = self.dm.SetShowErrorMsg(0)
		dm_ret = self.dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
		print('窗口绑定结果：%s' % dm_ret)
		if dm_ret == 0:
			return
		self.dm.MoveWindow(hwnd, 1, 1)
		self.dm.LockInput(1)
		if not os.path.exists(PATH + 'screen' + str(self.id)):
			os.makedirs(PATH + 'screen' + str(self.id))
		dm_ret = self.dm.SetPath(PATH + 'screen' + str(self.id))
		print('路径设置结果：%s' % dm_ret)
		self.start_game()


	def capture(self):
		# print(PATH + r"screen%s\0.bmp" % self.id)
		dm_ret = self.dm.Capture(0, 0, 2000, 2000, "0.bmp")
		if self.save_img:
			dm_ret = self.dm.Capture(0, 0, 2000, 2000, "{}.bmp".format(self.img_index))
			self.img_index += 1
		# print('截图结果：{}'.format(dm_ret))
		if str(dm_ret) is not '0':
			return cv2.imread(PATH + "screen%s/0.bmp" % self.id)

	@staticmethod
	def get_resource(name):
		path = PATH + 'resource/' + name + '.png'
		if not os.path.exists(path):
			print(path, '不存在')
			return
		img = cv2.imread(path)
		return img

	def find_pic(self, img, target: np.ndarray, the=0.95, center_point=True):
		res = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		if max_val < the:
			return 0, 0
		if center_point:
			print('相似度：', max_val)
			return max_loc[0] + int(target.shape[1] / 2), max_loc[1] + int(target.shape[0] / 2)
		else:
			return max_val

	def start_game(self):
		pic_name_list = ['reset', 'X', 'PLAY', 'xunlian', 'xunlianmoshi', 'queren', 'kaishiyouxi', 'xialu', 'hanbing',
						'queren2']
		for pic_name in pic_name_list:
			if self.start_success:
				print('完成游戏开启，退出大厅操作')
				return
			print('当前寻找图片：', pic_name)
			if pic_name == 'reset':
				self.click_position((524, 29))
			else:
				self.click_img(self.get_resource(pic_name), runTimes=2, clicked_check=False)
			time.sleep(1)

	def click_img(self, target_img, runTimes=10, clicked_check=True):
		clicked = not clicked_check
		delay_time = 0.2
		for i in range(runTimes):
			img = self.capture()
			if (np.array(img.shape[:2]) < 300).any():
				print('界面消失 退出', img.shape)
				self.start_success = True
				return
			time.sleep(delay_time)
			pos = self.find_pic(img, target_img)
			if pos[0] == 0:
				if clicked:
					return
				time.sleep(delay_time)
				continue
			else:
				self.click_position(pos)
				time.sleep(10*delay_time)
				# cv2.circle(img, pos,1,(255,255,0),3)
				# cv2.imwrite('p.png',img)
				if clicked:
					return
				clicked = True

	def click_position(self, pos):
		time.sleep(0.1)
		self.dm.MoveTo(*pos)
		time.sleep(0.1)
		self.dm.LeftClick()


class dmManager():
	def __init__(self):
		self.id = 0
		self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
		print('dmManager，id：{}'.format(self.id))
		self.operaterHwndsList = []
		self.operaterDict = {}
		self.opId = 0  # 为了创建operater储存id
		while True:
			self.check_hwnd2()
			time.sleep(1)

	def check_hwnd2(self):
		windowNames = [GAME_WINDOW_NAME, GAME_HALL_NAME]
		classs = [dmOperater, dm_hall_operater]
		for i in range(2):
			windowName = windowNames[i]
			hwnds = self.dm.EnumWindow(0, windowName, "", 1 + 4 + 8 + 16)
			print('hwnds:[{}]'.format(hwnds))
			if isinstance(hwnds, str):
				if hwnds != '':
					hwnd = hwnds
				else:
					continue
			else:
				hwnd = hwnds[0]
			op = classs[i](self.opId, int(hwnd), self)
			print('当前任务：【{}】完成，将于5秒后开启下次任务'.format(windowName))
			time.sleep(5)

	def check_hwnd3(self):
		windowNames = GAME_HALL_NAME
		classs = dm_hall_operater

		windowName = windowNames
		hwnds = self.dm.EnumWindow(0, windowName, "", 1 + 4 + 8 + 16)
		print('hwnds:[{}]'.format(hwnds))
		if isinstance(hwnds, str):
			if hwnds != '':
				hwnd = hwnds
			else:
				return
		else:
			hwnd = hwnds[0]
		op = dm_hall_operater(self.opId, int(hwnd), self)

	def checkHwnd(self):
		windowName = GAME_WINDOW_NAME
		hwnds = self.dm.EnumWindow(0, windowName, "", 1 + 4 + 8 + 16)
		print('hwnds:[{}]'.format(hwnds))
		if isinstance(hwnds, str):
			if hwnds != '':
				hwnds = [hwnds]
			else:
				hwnds = []
		for hwnd in hwnds:
			if hwnd not in self.operaterHwndsList or True:
				self.opId += 1
				op = dmOperater(self.opId, int(hwnd), self)  # 此处待开发多线程方式
				opDict = {
					'id': self.opId,
					'hwnd': hwnd,
					'op': op
				}
				self.operaterHwndsList.append(hwnd)
				self.operaterDict[hwnd] = opDict


if __name__ == '__main__':

	dm = dmManager()
	exit()

	windowName = "League of Legends (TM) Client"

	# windowName = GAME_HALL_NAME

	dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
	print(dm.ver())  # 输出版本号
	hwnds = ''
	while hwnds == '':
		hwnds = dm.EnumWindow(0, windowName, "", 1 + 4 + 8 + 16)
		time.sleep(1)
		print('未找到游戏进程 等待1s')
	print(hwnds)
	hwnd = int(hwnds)

	dm_ret = dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
	print('结果：%s' % dm_ret)
	start = time.time()
	last = 0
	i = 0
	while True:
		if time.time() - last > 0.5:
			i += 1
			dm_ret = dm.Capture(0, 0, 2000, 2000, "dm/ans/screen%s.bmp" % i)
			print('第%s张 结果：%s' % (i, dm_ret))
			last = time.time()
		time.sleep(0.01)
	print('经过的时间：%s' % (time.time() - start))
	dm_ret = dm.UnBindWindow()
	print('结果：%s' % dm_ret)
