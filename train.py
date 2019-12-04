import cv2,json
# import tensorflow as tf
import numpy as np
import sys,os

import pathlib
from setting import *
from paramsExtract.heroAndSoldierPostionDetact.heroAndSoldierPostionDetact import hero_soldier_detacter
import math
import multiprocessing as mp
import random

nothing_times = 0
caculate_index = 0
decay_rate = DECAY_RATE

print('decay_rate:',decay_rate)

all_scores = []
hp_scores = []
money_add_scores = []
money_use_scores = []
exp_scores = []
go_on_scores = []
nothing_scores = []

memory = []




def caculate_socre(currentParams:dict,nextParams:dict,current_actions:list):
    score = 0
    global nothing_times,caculate_index
    global all_scores,hp_scores,money_scores,exp_scores,go_on_scores,nothing_scores
    hp0 = currentParams['HP']
    hp1 = nextParams['HP']

    money0 = currentParams['money']
    money1 = nextParams['money']

    exp0 = currentParams['exp']
    exp1 = nextParams['exp']

    currentPostion = currentParams['postionIndex']



    deta_hp = hp1 - hp0
    hp_score = 0
    if deta_hp > 0:
        hp_score = deta_hp
    elif deta_hp < 0:
        hp_score = deta_hp / (hp0+0.000001)
    if hp1 == 0 and hp0 > 0:
        hp_score = -5

    money_score = 0
    money_add_score = 0
    use_money_score = 0
    if money0 != 0 and money1 != 0:
        detaMoney = np.max([np.abs(money1 - money0), 0])
        money_add_score = np.max([(detaMoney) ** 0.5, 3]) - 3
        if current_actions == 0:
            if money1 - money0 < 100:
                use_money_score = 5
    else:
        money_add_score = 0

    exp_score = 0
    if not exp0 == exp1:
        exp_score = 1

    go_on_score = 0
    if currentPostion < 7:
        if current_actions == 2 and hp0 > 0.8:
            go_on_score = currentPostion - 10
        elif current_actions == 0 and hp0 > 0.8 and money1 - money0 < 100 and money0 != 0 and money1 != 0:
            go_on_score = (currentPostion - 10)*20
    else:
        if hp0 > 0.9 and current_actions == 0 and money1 - money0 < 100 and money0 != 0 and money1 != 0:
            go_on_score = -100
    hp_score = hp_score * 10
    money_add_score = money_add_score * 5
    use_money_score = use_money_score * 1
    exp_score = exp_score * 10
    go_on_score = go_on_score * 0.8

    hp_scores.append(hp_score)
    money_add_scores.append(money_add_score)
    money_use_scores.append(use_money_score)
    exp_scores.append(exp_score)
    go_on_scores.append(go_on_score)

    score = hp_score + money_score + exp_score + go_on_score

    #对长时间无所事事进行处罚
    if nothing_times is None:
        nothing_times = 0
    if score == 0 or score < -2.5:
        nothing_times += 1
    else:
        nothing_times = 0

    nothing_score = nothing_times**2/200
    nothing_max_score = 100
    if nothing_score > nothing_max_score:
        nothing_score = nothing_max_score

    if current_actions in [0, 2]:#回城和后退
        nothing_score *= -1
    elif current_actions in [1, 5]:
        nothing_score *= 0.1
    else:
        nothing_score = 0
    score += nothing_score
    nothing_scores.append(nothing_score)
    if score != 0:
        print('{}:score:{:<10f} action:{} hp_score:{:<5f} money_add_score:{:<5f} use_money_score:{:<5f} exp_score:{} go_on_score:{} nothing_score:{}'.format(caculate_index,score,current_actions,hp_score,money_add_score,use_money_score,exp_score,go_on_score,nothing_score))
    caculate_index += 1

    all_scores.append(score)
    return nothing_score + go_on_score+use_money_score, hp_score+exp_score+money_add_score


def standardization(data):
    mu = np.mean(data, axis=0)
    if np.isnan(mu):
        mu = 0
    sigma = np.std(data, axis=0)
    if np.isnan(sigma):
        sigma = 1
    if sigma == 0:
        sigma = 1
    return data / sigma

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


def generateData(path,p,reCaculateParms = False,reCaculateScore = False,learn_data = True):
    path += '/'
    global memory
    if not os.path.exists(path + 'infor.txt'):
        print(path + 'infor.txt not exist')
        print('path is empty remove it path：{}'.format(path))
        del_file(path)
        return

    # 执行基础数据生成程序
    if os.path.exists(path + 'dataList.txt') and not reCaculateParms:
        if not os.path.exists(path + 'infor2.txt') or reCaculateScore:
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
        p.init_obs()
        for s in ss:
            if s is not '':
                dic = json.loads(s)
                img =cv2.imread(path + '{}.png'.format(dic['file']))
                print('current file:{}'.format(path + '{}.png'.format(dic['file'])))
                params = p.param_extract(img, target_mat=False, target=False, tower=False, hp=True)
                dic['params'] = params
                _, dic['obs'] = p.obs_params_extract(img,igone_same_check=True)
                dic['obs'] = dic['obs'].tolist()
                dataList.append(dic)


        data_list_str = json.dumps(dataList)
        # exit()
        with open(path + 'dataList.txt', "w") as f:  # 设置文件对象
            f.write(data_list_str)

    if os.path.exists(path + 'infor2.txt') and not reCaculateScore:
        print(path + 'infor2.txt exist')
        with open(path + 'infor2.txt', "r") as f:  # 设置文件对象
            inforStr = f.read()
            dataDic = json.loads(inforStr)
    else:
        #执行分数计算程序
        length = len(dataList)
        if length == 0:
            print('length == 0 path is empty remove it path：{}'.format(path))
            del_file(path)
            return
        dataList[length-1]['score'] = 0#此处以后根据胜负进行赋值
        socre_cahe = 0
        scores_before_standerlize = np.zeros((length,))
        for i in range(length-2,-1,-1):
            short_score, long_score = caculate_socre(dataList[i]['params'], dataList[i+1]['params'], dataList[i]['actions'])
            score = long_score + decay_rate * socre_cahe
            socre_cahe = score
            score += short_score
            scores_before_standerlize[i] = score

        standerlize_score = standardization(scores_before_standerlize)
        for i in range(length-2,-1,-1):
            # print(standerlize_score[i])
            dataList[i]['score'] = standerlize_score[i]
            if np.isnan(standerlize_score[i]):
                print('nan err')
                exit()

        dataDic = []
        for dic in dataList:
            action = dic['actions']
            score = dic['score']
            obs = dic['obs']

            data = {
                'obs':obs,
                'action':action,
                'score':score
            }
            if score != 0:
                dataDic.append(data)

        json_str = json.dumps(dataDic)
        with open(path + 'infor2.txt', 'w') as f:
            f.write(json_str)

    if learn_data:
        memory = memory + dataDic

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


def generate_data_score(reCaculateScore=False):
    global memory
    global all_scores,hp_scores,money_scores,exp_scores,go_on_scores,nothing_scores
    from picProcessor import picProcessor
    p = picProcessor(test=True)
    memory = []

    if DATA_ADDRESS == '':
        data_root = PROJECT_ADDRESS + r'ans'
    else:
        data_root = DATA_ADDRESS

    all_scores = []
    data_root = pathlib.Path(data_root)
    all_data_paths = list(data_root.glob('*'))
    all_data_paths = [str(path) for path in all_data_paths]
    random.shuffle(all_data_paths)

    # all_data_paths = [all_data_paths[0]]
    memory_sum = 0
    while len(all_data_paths) > 0:
        path = all_data_paths.pop(0)
        print('process path:{}'.format(path))
        generateData(path,p,reCaculateScore=reCaculateScore, reCaculateParms=False)
        print('当前记忆数量:',len(memory), ' 剩余未加载地址数量：',len(all_data_paths))
        if len(memory) > MEMORY_SIZE-1 or len(all_data_paths) == 0:
            memory_sum += len(memory)
            learn(memory)
            memory = []
    if reCaculateScore:
        print_mean(all_scores,'score')
        print_mean(hp_scores,'hp_scores')
        print_mean(exp_scores,'exp_scores')
        print_mean(money_add_scores,'money_add_scores')
        print_mean(money_use_scores,'money_use_scores')
        print_mean(go_on_scores,'go_on_scores')
        print_mean(nothing_scores,'nothing_scores')
    print('本轮训练加载记忆总量：',memory_sum)

def print_mean(ls,name):
    me = np.mean(ls)
    ls_no0 = [0]
    for i in ls:
        if i != 0:
            ls_no0.append(i)
    me_not0 = np.mean(ls_no0)
    var = np.var(ls)
    var_no0 = np.var(ls_no0)

    print('mean:{:<10f} no_zero_mean:{:<10f} var:{:<10f} no_Zero_var:{:<10f}--{:<10s}'.format(me,me_not0,var,var_no0,name))



def learn(datalist):
    print('当前加载记忆数量：',len(datalist))
    from RL_brain import policy_gradient
    random.shuffle(datalist)
    brain = policy_gradient(n_features=9382, n_actions=6)
    obss=[]
    actions=[]
    qs = []
    while len(datalist) > 0:
        data = datalist.pop(0)
        obs = data['obs']
        action = data['action']
        q = data['score']
        obss.append(obs)
        assert len(obs) == OBSERVATION, len(obs)
        actions.append(action)
        qs.append(q)
        if len(obss) > LEARNING_BATCH - 1 or len(datalist) == 0:
            brain.learn(obss,actions,qs,False)
            obss = []
            actions = []
            qs = []
            print('当前训练剩余记忆量：', len(datalist))

    brain.save_net()





if __name__ == '__main__':
    # test_mat()
    # exit()
    generate_data_score()

