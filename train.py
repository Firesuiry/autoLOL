import cv2,json
# import tensorflow as tf
import numpy as np
import sys,os
from picProcesser import picProcesser
import pathlib
from setting import *

decay_rate = DECAY_RATE
print('decay_rate:',decay_rate)

def caculate_socre(currentParams:dict,nextParams:dict):
	score = 0

	hp0 = currentParams['HP']
	hp1 = nextParams['HP']

	money0 = currentParams['money']
	money1 = nextParams['money']

	deta_hp = hp1 - hp0
	hp_score = 0
	if deta_hp > 0:
		hp_score = deta_hp
	elif deta_hp < 0:
		hp_score = deta_hp / (hp0+0.000001)


	if money0 != -1 and money1 != -1:
		detaMoney = np.max([money1 - money0, 0])
		money_score = np.max([(detaMoney) ** 0.5, 2]) - 2
	else:
		money_score = 0

	score = hp_score*2 + money_score*100

	return score


def del_file(path):
	for i in os.listdir(path):
		path_file = os.path.join(path, i)
		if os.path.isfile(path_file):
			os.remove(path_file)
		else:
			del_file(path_file)
	os.rmdir(path)

def generateData(path,p,reCaculateParms = False,reCaculateScore = False):
	path += '/'

	if not os.path.exists(path + 'infor.txt'):
		print(path + 'infor.txt not exist')
		print('path is empty remove it path：{}'.format(path))
		del_file(path)
		return

	if os.path.exists(path + 'infor2.txt') and not reCaculateScore:
		print(path + 'infor2.txt exist')
		return

	# 执行基础数据生成程序
	if os.path.exists(path + 'dataList.txt') and not reCaculateParms:
		with open(path + 'dataList.txt', "r") as f:  # 设置文件对象
			inforStr = f.read()
			dataList = json.loads(inforStr)
	else:
		with open(path + 'infor.txt', "r") as f:  # 设置文件对象
			inforStr = f.read()  # 可以是随便对文件的操作

		if inforStr == '':
			print('path is empty remove it path：{}'.format(path))
			del_file(path)
			return

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
			# if len(dataList) > 2:
			# 	break
		data_list_str = json.dumps(dataList)
		with open(path + 'dataList.txt', "w") as f:  # 设置文件对象
			f.write(data_list_str)


	#执行分数计算程序
	length = len(dataList)
	if length == 0:
		print('length == 0 path is empty remove it path：{}'.format(path))
		del_file(path)
		return
	dataList[length-1]['score'] = 0#此处以后根据胜负进行赋值
	socre_cahe = 0
	for i in range(length-2,-1,-1):
		score = caculate_socre(dataList[i]['params'],dataList[i+1]['params'])
		score = score + decay_rate * socre_cahe
		socre_cahe = score
		dataList[i]['score'] = score

	for dic in dataList:
		# ______________________________此处为为了兼容之前保存的东西进行的修改,目前仍是如此保存的
		actions = dic['actions']
		target_action = [0,0,0]
		if type(actions) == dict:
			if actions['go'] > 0:
				target_action[0] = 1
			if actions['back'] > 0:
				target_action[1] = 1
			actions = target_action
		dic['actions'] = actions
		# ______________________________

	dataDic = {}
	for dic in dataList:
		file = dic['file']
		action = dic['actions']
		score = dic['score']

		if action[0] == 1:
			score += 1

		data = {
			'action':action,
			'score':score
		}
		dataDic[file] = data

	json_str = json.dumps(dataDic)
	with open(path + 'infor2.txt', 'w') as f:
		f.write(json_str)

if __name__ == '__main__':
	p = picProcesser(test=True)
	if DATA_ADDRESS == '':
		data_root = PROJECT_ADDRESS + r'ans'
	else:
		data_root = DATA_ADDRESS
	data_root = pathlib.Path(data_root)
	all_data_paths = list(data_root.glob('*'))
	all_data_paths = [str(path) for path in all_data_paths]
	for path in all_data_paths:
		print('process path:{}'.format(path))
		generateData(path,p,reCaculateScore=True)
