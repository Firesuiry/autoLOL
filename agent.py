from picProcessor import picProcessor
from operater import operater
from RL_brain import policy_gradient
from setting import *
import time,cv2
from reviewAndTrain.dataStore import dataStore

class agent():
    def __init__(self, agent_id=1, test=False):
        if not test:
            self.operator = operater()
        else:
            self.operator = None
        self.pic_processor = picProcessor(self.operator, test=False)
        self.state = SMART_CONTROL_MODE
        self.id = agent_id
        self.brain = policy_gradient()
        self.ds = dataStore()
        if not test:
            self.mainLoop()


    def mainLoop(self):
        while (True):
            # ###########################获取ob
            newT = time.time()
            ret = self.operator.Capture(0, 0, 2000, 2000, r"dm/screen1/0.bmp")
            # print('截图结果：{}'.format(ret))
            if ret == 0:
                print('capture fail')
                time.sleep(0.1)
                continue
            img = self.loadPic(r'dm\screen1/0.bmp')
            # ############################ob加工
            params = self.pic_processor.param_extract(img)

            # #############################动作选择
            action = self.brain.determine_action(params)

            # #############################动作执行
            action_last_time = self.operator.actionExcute(action, params)

            # #############################记忆储存
            self.ds.storeResult(img, params, action)



            if pic is not None:
                if self.state == SMART_CONTROL_MODE:
                    self.pic_processor.get_pic(pic)
                elif self.state == ARTIFICIAL_CONTROL_MODE:
                    pass
                print('命令发送完成 花费时间：{}'.format(time.time() - newT))
                time.sleep(0.05)
            else:
                time.sleep(0.1)

    def loadPic(self, path='res/Screen01.png'):
        pic = cv2.imread(path)
        return pic

if __name__ == "__main__":
    a = agent()
