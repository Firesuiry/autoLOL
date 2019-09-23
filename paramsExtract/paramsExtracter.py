from paramsExtract.HPextracter.HPextracter import hpExtract
from paramsExtract.mapPostionExtracter.mapPostionExtracter import centerParaExtract

def paramExtract(self):
	'''
	通过游戏图像获取游戏动作执行过程中所需的参数
	:param pic:
	:return:动作等所需参数
	'''
	params = {}
	pic = self.currentPic
	params['back'], params['postion'], params['go'] = centerParaExtract(self)
	params['HP'] = hpExtract(self)
	return params


