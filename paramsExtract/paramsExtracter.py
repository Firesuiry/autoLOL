from paramsExtract.HPextracter.HPextracter import hpExtract
from paramsExtract.mapPostionExtracter.mapPostionExtracter import centerParaExtract
from paramsExtract.MoneyExtracter.MoneyExtracter import get_charter
from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
from paramsExtract.defense_tower_detact.defense_tower_position_detect import tower_detacter
from paramsExtract.currentExp.currentExp import current_exp
import cv2
import numpy as np


def paramExtract(self, position=True, money = True, exp=True, target_mat=True):
	'''
	通过游戏图像获取游戏动作执行过程中所需的参数
	所有params的值必须为list或者dic 方便后面序列化
	:param pic:
	:return:动作等所需参数
	'''
	params = {}
	pic = self.currentPic.copy()

	if position:
		params['back'], params['postion'], params['go'],close_postion_index = centerParaExtract(self)
		params['HP'] = hpExtract(self)
		params['postionIndex'] = int(close_postion_index)

	if money:
		moneyPic = self.element_extract('MONEY', pic)
		params['money'] = get_charter(moneyPic)

	if exp:
		expPic = self.element_extract('EXP', pic)
		params['exp'] = current_exp(expPic)

	if target_mat:
		params['mat'] = hero_soldier_detacter.get_target_mat(pic)
		params['tower'] = tower_detacter.getTargetPostions(pic)
		print(params['tower'])

	return params


