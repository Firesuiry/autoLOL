from screenCap import screenCap
from picProcessor import picProcessor
from operater import operater
from dm.MainCommucation import MainCommucation
from setting import *
import time,cv2

class agent():
    def __init__(self,id = 1):
        self.operater = operater()
        self.pic_processer = picProcessor(self.operater, test=False)
        self.state = SMART_CONTROL_MODE
        self.id = id

        self.mainLoop()

    def mainLoop(self):
        while (True):
            newT = time.time()
            ret = self.operater.Capture(0, 0, 2000, 2000, r"screen1/0.bmp")
            # print('截图结果：{}'.format(ret))
            if ret == 0:
                print('capture fail')
                time.sleep(0.1)
                continue
            # print('截图完成 花费时间：{}'.format(time.time() - newT))
            pic = self.loadPic(r'dm\screen1/0.bmp')
            # print('读取图片完成 花费时间：{}'.format(time.time() - newT))
            if pic is not None:
                if self.state == SMART_CONTROL_MODE:
                    self.pic_processer.get_pic(pic)
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
