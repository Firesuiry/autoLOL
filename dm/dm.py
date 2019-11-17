# -*- coding: utf-8 -*-
import DmCommucation as dc
import time
import os, json

import cv2
import win32com.client
import sys
from dm_setting import *


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
		print ('dmOperater启动，id：{} hwnd:{}'.format(id, hwnd))
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
		self.start()

	def capture(self):
		dm_ret = self.dm.Capture(0, 0, 2000, 2000, "screen%s/0.bmp" % self.id)
		print('截图结果：{}'.format(dm_ret))

	def __getattr__(self, item):
		def dock(*args, **kwargs):
			if self.bind_ret == "失败": return "大漠未绑定窗口"
			return getattr(self.dm, item)(*args, **kwargs)

		return dock if item not in self.__dict__ else getattr(self, item)

class dm_hall_operater():
	def __init__(self, id, hwnd, manager):
		self.get_resource('screen')
		self.id = id
		self.hwnd = hwnd
		self.manager = manager
		print ('dm_hall_operater 启动，id：{} hwnd:{}'.format(id, hwnd))
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

	def capture(self):
		dm_ret = self.dm.Capture(0, 0, 2000, 2000, PATH + "screen%s/0.bmp" % self.id)
		print('截图结果：{}'.format(dm_ret))
		if str(dm_ret) is not '0':
			return cv2.imread(PATH + "screen%s/0.bmp" % self.id)

	@staticmethod
	def get_resource(name):
		path = PATH + name + '.png'
		if not os.path.exists(path):
			print(path,'不存在')
			return
		img = cv2.imread(path)
		return img

	def find_pic(self):
		pass






class dmManager():
	def __init__(self):
		self.id = 0
		self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
		print ('dmManager，id：{}'.format(self.id))
		self.operaterHwndsList = []
		self.operaterDict = {}
		self.opId = 0  # 为了创建operater储存id
		self.checkHwnd()

	def checkHwnd(self):
		windowName = GAME_WINDOW_NAME
		hwnds = self.dm.EnumWindow(0, windowName, "", 1 + 4 + 8 + 16)
		print('hwnds:',hwnds)
		print(type(hwnds))
		if isinstance (hwnds,str):
			if hwnds != '':
				hwnds = [hwnds]
			else:
				hwnds = []
		for hwnd in hwnds:
			if hwnd not in self.operaterHwndsList:
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
	if len(sys.argv) == 1:
		dm_hall_operater()
		exit()

		dm = dmManager()
	else:
		print(sys.argv)
		if sys.argv[1] == '1':
			windowName = "League of Legends (TM) Client"
		else:
			windowName = "League of Legends (TM) Client - [Windows 7 x64]"
		dm = win32com.client.Dispatch('dm.dmsoft')  #调用大漠插件
		print(dm.ver())#输出版本号
		hwnds = dm.EnumWindow(0,windowName,"",1+4+8+16)
		print(hwnds)
		hwnd = int(hwnds)

		dm_ret = dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
		print('结果：%s'%dm_ret)
		start = time.time()
		last = 0
		i = 0
		while True:
			if time.time() - last > 0.5:
				i += 1
				dm_ret = dm.Capture(0, 0, 2000, 2000, "ans/screen%s.bmp" % i)
				print('第%s张 结果：%s' % (i, dm_ret))
				last = time.time()
			time.sleep(0.01)
		print('经过的时间：%s'%(time.time()-start))
		dm_ret = dm.UnBindWindow()
		print('结果：%s'%dm_ret)
