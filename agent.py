from picProcessor import picProcessor
from operater import operater
from RL_brain import policy_gradient
from setting import *
import time,cv2
from reviewAndTrain.dataStore import dataStore
from enum import Enum


class GAME_STATE(Enum):
    LOADING = 0
    RUNNING_INIT = 1
    RUNNING = 2
    ENDING = 3


class agent():
    def __init__(self, agent_id=1, test=False ,save_mem=True):
        if not test:
            self.operator = operater()
        else:
            self.operator = None
        self.pic_processor = picProcessor(test=False)
        self.id = agent_id
        self.brain = policy_gradient(0,0)
        if save_mem:
            self.ds = dataStore()
        self.save_mem = save_mem

        self.game_state = GAME_STATE.LOADING
        if not test:
            self.mainLoop()


    def mainLoop(self):
        while (True):
            # ###########################获取ob
            img = self.operator.get_game_img()

            # ###########################游戏阶段判断
            if self.game_state == GAME_STATE.LOADING:
                loading_complete = self.pic_processor.loading_complete(img)
                if loading_complete:
                    self.game_state = GAME_STATE.RUNNING_INIT
                time.sleep(1)
                continue

            if self.game_state == GAME_STATE.RUNNING_INIT:
                self.operator.init_action()
                self.game_state = GAME_STATE.RUNNING
                continue

            # ############################ob加工
            try:
                params = self.pic_processor.param_extract(img, money=False)
            except Exception as e:
                print(e)
                time.sleep(1)
                raise e
                continue

            # #############################动作选择
            action = self.brain.determine_action(params)

            # #############################动作执行
            self.operator.actionExcute(action, params)

            # #############################记忆储存
            if self.save_mem:
                self.ds.storeResult(img, params, action)

            time.sleep(1)

    def loadPic(self, path='res/Screen01.png'):
        pic = cv2.imread(path)
        return pic

if __name__ == "__main__":
    a = agent(save_mem=False)
