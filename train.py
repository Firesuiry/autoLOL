import cv2,json
# import tensorflow as tf
import numpy as np
import sys,os

import pathlib
from setting import *
from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
import math
import multiprocessing as mp

nothing_times = 0
caculate_index = 0
decay_rate = DECAY_RATE
print('decay_rate:',decay_rate)


def caculate_socre(currentParams:dict,nextParams:dict,current_actions:list):
    score = 0
    global nothing_times,caculate_index
    hp0 = currentParams['HP']
    hp1 = nextParams['HP']

    money0 = currentParams['money']
    money1 = nextParams['money']

    exp0 = currentParams['exp']
    exp1 = nextParams['exp']

    currentPostion = currentParams['postion']



    deta_hp = hp1 - hp0
    hp_score = 0
    if deta_hp > 0:
        hp_score = deta_hp
    elif deta_hp < 0:
        hp_score = deta_hp / (hp0+0.000001)

    money_score = 0
    if money0 != -1 and money1 != -1:
        detaMoney = np.max([money1 - money0, 0])
        money_score = np.max([(detaMoney) ** 0.5, 2]) - 2
    else:
        money_score = 0

    exp_score = 0
    if not exp0 == exp1:
        exp_score = 1

    go_on_score = 0
    # if currentPostion < 10:
    # 	if current_actions[0] == 1:
    # 		go_on_score = 10 - currentPostion
    # 	elif current_actions[1] == 1:
    # 		go_on_score = current_actions - 10
    hp_score = hp_score * 2
    money_score = money_score * 5
    exp_score = exp_score * 20
    go_on_score = go_on_score * 0.5

    score = hp_score + money_score + exp_score + go_on_score

    #对长时间无所事事进行处罚
    if nothing_times is None:
        nothing_times = 0
    if score == 0:
        nothing_times += 1
    else:
        nothing_times = 0

    nothing_score = nothing_times**2/1000
    nothing_max_score = 20
    if nothing_score > nothing_max_score:
        nothing_score = nothing_max_score

    if current_actions[0] == 1:
        score += nothing_score
    elif current_actions[1] == 1:
        score -= nothing_score

    print('{}:score:{:<10f} action:{} hp_score:{:<5f} money_score:{:<5f} exp_score:{} go_on_score:{} nothing_score:{}'.format(caculate_index,score,current_actions,hp_score,money_score,exp_score,go_on_score,nothing_score))
    caculate_index += 1

    score = score/3.3324922355957254
    all_scores.append(score)
    return score


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)
    os.rmdir(path)

def generate_soldier_mat(img):
    postion_data = hero_soldier_detacter.getTargetPostions(img, return_as_ndarry=True)
    # print('postion_data.shape:',postion_data.shape)
    h, w, c = img.shape
    h = math.ceil(h/32) - 1
    w = math.ceil(w/32)
    unit_mat = np.zeros((3,h, w), dtype=int)
    for i in range(3):
        for pos in postion_data[i]:
            x = pos[0] // 32
            y = pos[1] // 32
            if y > 21:
                y = 21
            unit_mat[i, y, x] = 1
    return unit_mat

def generate_soldier_data(path):
    path += '/'


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
                params = p.param_extract(img, False)
                dic['params'] = params
                dataList.append(dic)
        # if len(dataList) > 1:
        # 	break
        # print(dataList)
        # for data in dataList:
        # 	for key,value in data['params'].items():
        # 		print(key,value,type(value))
        data_list_str = json.dumps(dataList)
        # exit()
        with open(path + 'dataList.txt', "w") as f:  # 设置文件对象
            f.write(data_list_str)

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


    #执行分数计算程序
    length = len(dataList)
    if length == 0:
        print('length == 0 path is empty remove it path：{}'.format(path))
        del_file(path)
        return
    dataList[length-1]['score'] = 0#此处以后根据胜负进行赋值
    socre_cahe = 0
    for i in range(length-2,-1,-1):
        score = caculate_socre(dataList[i]['params'],dataList[i+1]['params'],dataList[i]['actions'])
        score = score + decay_rate * socre_cahe
        socre_cahe = score
        dataList[i]['score'] = score



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

def save_mats(paths):
    print(paths)
    paths = json.loads(paths)
    i = 0
    l = len(paths)
    for path in paths:
        print(i/l*100,"%")
        save_mat(path)
        i+=1

def save_mat(path):
    npy_path = path[:-4] + '.npy'
    if os.path.exists(npy_path):
        print('pass path:',npy_path)
        return
    img = cv2.imread(path)
    mat = generate_soldier_mat(img)
    np.save(npy_path, mat > 0)

def tt(a):
    print('a',a)

def test_mat():
    if DATA_ADDRESS == '':
        data_root = PROJECT_ADDRESS + r'ans'
    else:
        data_root = DATA_ADDRESS
    data_root = pathlib.Path(data_root)
    all_data_paths = list(data_root.glob('*/*.png'))
    all_data_paths = [str(path) for path in all_data_paths]
    i = 0
    l = len(all_data_paths)
    print('需生成总数量：',l)
    # save_mat(all_data_paths[0])
    # exit()
    for i in range(l//10000 + 1):
        paths = []
        if l > (i+1)*10000:
            paths = all_data_paths[i*10000:(i+1)*10000]
        else:
            paths = all_data_paths[i*10000:]
        paths =json.dumps(paths)
        print(type(paths))
        p = mp.Process(target=save_mats, args=(paths,))
        p.start()




    # for path in all_data_paths:
    #     print(i/l*100, "%",i)
    #     save_mat(path)
    #     i += 1



if __name__ == '__main__':
    test_mat()
    exit()

    from picProcessor import picProcessor
    p = picProcessor(test=True)

    if DATA_ADDRESS == '':
        data_root = PROJECT_ADDRESS + r'ans'
    else:
        data_root = DATA_ADDRESS

    all_scores = []
    data_root = pathlib.Path(data_root)
    all_data_paths = list(data_root.glob('*'))
    all_data_paths = [str(path) for path in all_data_paths]
    for path in all_data_paths:
        print('process path:{}'.format(path))
        generateData(path,p,reCaculateScore=True)

    mean = np.mean(all_scores)

    print('average score:{}'.format(np.mean(all_scores)))
