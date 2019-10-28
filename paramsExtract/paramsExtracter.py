from paramsExtract.HPextracter.HPextracter import hpExtract
from paramsExtract.mapPostionExtracter.mapPostionExtracter import centerParaExtract
from paramsExtract.MoneyExtracter.MoneyExtracter import get_charter
from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
import cv2


def paramExtract(self,gameRuning = True):
	'''
	通过游戏图像获取游戏动作执行过程中所需的参数
	所有params的值必须为list或者dic 方便后面序列化
	:param pic:
	:return:动作等所需参数
	'''
	params = {}
	pic = self.currentPic.copy()
	params['back'], params['postion'], params['go'] = centerParaExtract(self)
	params['HP'] = hpExtract(self)

	if not gameRuning:
		moneyPic = self.elementExtract('MONEY',pic)
		params['money'] = get_charter(self.ai,moneyPic)
		print('money:{}'.format(params['money']))
	return params


