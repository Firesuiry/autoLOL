from paramsExtract.HPextracter.HPextracter import hpExtract
from paramsExtract.mapPostionExtracter.mapPostionExtracter import centerParaExtract
from paramsExtract.MoneyExtracter.MoneyExtracter import get_charter
# from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
from paramsExtract.currentExp.currentExp import current_exp
import cv2
import numpy as np


def paramExtract(self,gameRuning = True):
	'''
	通过游戏图像获取游戏动作执行过程中所需的参数
	所有params的值必须为list或者dic 方便后面序列化
	:param pic:
	:return:动作等所需参数
	'''
	params = {}
	pic = self.currentPic.copy()
	params['back'], params['postion'], params['go'],close_postion_index = centerParaExtract(self)
	params['HP'] = hpExtract(self)

	if not gameRuning:
		moneyPic = self.element_extract('MONEY', pic)
		params['money'] = get_charter(moneyPic)

		expPic = self.element_extract('EXP', pic)
		params['exp'] = current_exp(expPic)
		params['postionIndex'] = int(close_postion_index)
		# print('money:{} exp:{}'.format(params['money'],params['exp']))
	return params


