# -*- coding: utf-8 -*-
import DmCommucation as dc
import time
import os, json
import win32com.client


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


class dmOperater(dmBase, dc.DmCommucation):
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


class dmManager(dmBase):
	def __init__(self):
		self.id = 0
		self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
		print ('dmManager，id：{}'.format(self.id))
		self.operaterHwndsList = []
		self.operaterDict = {}
		self.opId = 0  # 为了创建operater储存id
		self.checkHwnd()

	def checkHwnd(self):
		windowName = "League of Legends (TM) Client - [Windows 7 x64]"
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
	dm = dmManager()

