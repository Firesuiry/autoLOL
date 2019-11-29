from paramsExtract.HPextracter.HPextracter import hpExtract
from paramsExtract.mapPostionExtracter.mapPostionExtracter import centerParaExtract
from paramsExtract.MoneyExtracter.MoneyExtracter import get_charter
from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
from paramsExtract.defense_tower_detact.defense_tower_position_detect import tower_detacter
from paramsExtract.currentExp.currentExp import current_exp
from paramsExtract.action_params.action_params import get_target_action
import cv2
import numpy as np


def paramExtract(self, position=True, money = True, exp=True, target_mat=True, target=True, img=None,params = None):
	'''
	通过游戏图像获取游戏动作执行过程中所需的参数
	所有params的值必须为list或者dic 方便后面序列化
	:param pic:
	:return:动作等所需参数
	'''
	if params is None:
		params = {}

	if img is not None:
		pic = img
	else:
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

	if target:
		params['target'] = get_target_action(params['mat'])

	return params

def observation(self):
	params = {}
	pic = self.currentPic.copy()
	params['HP'] = hpExtract(self)
	params['mat'] = hero_soldier_detacter.get_target_mat(pic)


if __name__ == '__main__':
	# img = cv2.imread(r'D:\develop\autoLOL\dm\ans\screen531.bmp')
	img = cv2.imread(r'D:\develop\autoLOL\dm\screen1\0.bmp')
	params = paramExtract(None,img=img,position=False,money=False,exp=False)
	print(params['target'])
	cv2.circle(img,tuple(params['target'][0]),radius=5, thickness=5,color=(255,255,255))
	cv2.circle(img,tuple(params['target'][1]),radius=5, thickness=5,color=(255,255,0))
	cv2.imwrite('p.png',img)



