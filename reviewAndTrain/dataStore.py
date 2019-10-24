# -*- coding: utf-8 -*-
import json,cv2,os
import numpy as np
from setting import *



class dataStore():
	'''
	this class is used to store the situation during the game for the following score and training
	'''
	def __init__(self):
		self.id = 0
		while(True):
			if DATA_ADDRESS == '':
				self.filesLocation = 'ans/game{}/'.format(self.id)
			else:
				self.filesLocation = DATA_ADDRESS + 'game{}/'.format(self.id)
			if not os.path.exists(self.filesLocation):
				print('create dir:{}'.format(self.filesLocation))
				os.makedirs(self.filesLocation)
				break
			else:
				self.id += 1
		self.picIndex = 0
		self.cache = {}
		self.txtFile = open(self.filesLocation + 'infor.txt', 'a')

	def storeResult(self,pic,params,actions):
		information = {
			'file':self.picIndex,
			'params':params,
			'actions':actions,
			'gameID':self.id
		}

		inforStr = json.dumps(information)
		self.txtFile.write(inforStr + '*fenge*')
		cv2.imwrite(self.filesLocation + '{}.png'.format(self.picIndex),pic)
		self.picIndex += 1

if __name__ == '__main__':
	img = cv2.imread(r'E:\develop\autoLOLres\ans\screen1.bmp')
	for i in range(1):
		ds = dataStore()
		for j in range(10):
			ds.storeResult(img,{'i':i},{'j':j})





