from screenCap import screenCap
from picProcesser import picProcesser
from operater import operater
from dm.MainCommucation import MainCommucation
import time

class agent():
    def __init__(self):
        pass

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
                self.getPic(pic)
                print('命令发送完成 花费时间：{}'.format(time.time() - newT))
                time.sleep(0.05)
            else:
                time.sleep(0.1)





if __name__ == "__main__":
    pass
