import cv2,json
# import tensorflow as tf
import numpy as np
import sys,os
from picProcesser import picProcesser
import pathlib


decay_rate = 0.95

def caculate_socre(currentParams:dict,nextParams:dict):
	score = 0

	hp0 = currentParams['HP']
	hp1 = nextParams['HP']

	money0 = currentParams['money']
	money1 = nextParams['money']

	hp_score = np.min([(hp1 - hp0) / (hp0 + 0.001), 0])
	if money0 != -1 and money1 != -1:
		detaMoney = np.max([money1 - money0, 0])
		money_score = np.max([(detaMoney) ** 0.5, 2]) - 2
	else:
		money_score = 0

	score = hp_score + money_score

	return score

def generateData(path,p):
	path += '/'

	if not os.path.exists(path + 'infor.txt'):
		print(path + 'infor.txt not exist')
		return

	if os.path.exists(path + 'infor2.txt'):
		print(path + 'infor2.txt exist')
		return

	with open(path + 'infor.txt', "r") as f:  # 设置文件对象
		inforStr = f.read()  # 可以是随便对文件的操作

	ss = inforStr.split('*fenge*')
	# print(ss)
	dataList = []
	for s in ss:
		if s is not '':
			dic = json.loads(s)
			img =cv2.imread(path + '{}.png'.format(dic['file']))
			print('current file:{}'.format(path + '{}.png'.format(dic['file'])))
			params = p.paramExtract(img,False)
			dic['params'] = params
			dataList.append(dic)
		# if len(dataList) > 10:
		# 	break

	length = len(dataList)
	dataList[length-1]['score'] = 0#此处以后根据胜负进行赋值
	socre_cahe = 0
	for i in range(length-2,-1,-1):
		score = caculate_socre(dataList[i]['params'],dataList[i+1]['params'])
		score = score + decay_rate * socre_cahe
		socre_cahe = score
		dataList[i]['score'] = score

	for dic in dataList:
		del dic['params']
		# ______________________________此处为为了兼容之前保存的东西进行的修改
		actions = dic['actions']
		target_action = [0,0,0]
		if type(actions) == dict:

			if actions['go'] > 0:
				target_action[0] = 1
			if actions['back'] > 0:
				target_action[1] = 1
			actions = target_action
		# ______________________________
		actionContent = ''
		for act in actions:
			actionContent += str(act)
			actionContent += ','
		actionContent = actionContent[:-1]

		file_name = str(dic['file']) + '.txt'
		with open(path + file_name, 'w') as f:
			content = actionContent + '+' + str(dic['score'])
			f.write(content)


	json_str = json.dumps(dataList)
	with open(path + 'infor2.txt', 'w') as f:
		f.write(json_str)





if __name__ == '__main__':


	p = picProcesser(test=True)
	data_root = r'D:\develop\autoLOL\ans'
	data_root = pathlib.Path(data_root)
	all_data_paths = list(data_root.glob('*'))
	all_data_paths = [str(path) for path in all_data_paths]
	for path in all_data_paths:
		generateData(path,p)
