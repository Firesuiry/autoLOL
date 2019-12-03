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
		self.errFile = open(self.filesLocation + 'err.txt', 'a')


	def err_write(self,err):
		err = [str(err)+'\n',str(err.__traceback__.tb_frame.f_globals["__file__"])+'\n',str(err.__traceback__.tb_lineno)+'\n']
		print(err)
		self.errFile.writelines(err)

	def storeResult(self,pic,params,actions,obs, action_prob):
		information = {
			'file':self.picIndex,
			# 'params':params,
			'actions':actions,
			'gameID':self.id,
			'obs':obs.tolist(),
			'action_prob':action_prob.tolist()
		}

		inforStr = json.dumps(information)
		self.txtFile.write(inforStr + '*fenge*')
		cv2.imwrite(self.filesLocation + '{}.png'.format(self.picIndex),pic)
		self.picIndex += 1

if __name__ == '__main__':
	a = []
	try:
		a[5] = 0
	except Exception as e:
		ds = dataStore()
		ds.err_write(e)






