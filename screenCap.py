import time
import win32gui, win32ui, win32con, win32api
from PIL import Image,ImageGrab
import numpy as np
import cv2


class screenCap():
    def __init__(self):
        self.hwnd = 0
        self.hwnd_title = dict()

    def screen(self):
        screen = ImageGrab.grab()
        screen = cv2.cvtColor(np.asarray(screen), cv2.COLOR_RGB2BGR)
        return screen

    def getHwnd(self):
        #获取主句柄
        classname = "VMUIFrame"
        titlename = "Windows 7 x64 - VMware Workstation"
        # classname = "VMwareUnityHostWndClass"
        # titlename = "League of Legends - [Windows 7 x64]"
        self.hwnd = win32gui.FindWindow(classname, titlename)
        #获取所有子句柄
        childHwndList = self.get_child_windows(self.hwnd)
        #遍历子句柄获取所需
        for hwnd in childHwndList:
            title = win32gui.GetWindowText(hwnd)
            clsname = win32gui.GetClassName(hwnd)
            #print('title:%s clsname:%s'%(title,clsname))
            if 'VMware.GuestWindow' in clsname:
                self.hwnd = hwnd
        print(self.hwnd)
        return self.hwnd

    def get_child_windows(self,parent):
        #获得parent的所有子窗口句柄
        #返回子窗口句柄列表
        if not parent:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList
    def window_capture(self,filename = ''):
        hwnd = self.hwnd # 窗口的编号，0号表示当前活跃窗口

        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        #设置所需监控器大小（调节分辨率需修改）
        w = 1280
        h = 720
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)
        #创建opencv标准图像格式，作为返回值
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        print(im_opencv)
        im_opencv.shape = (h, w, 4)
        print(im_opencv)
        print(type(im_opencv))
        cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
        cv2.imwrite('CV2.png', im_opencv)
        return im_opencv


    def get_all_hwnd(self,hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    def allHwnd(self):
        win32gui.EnumWindows(self.get_all_hwnd, 0)

        for h, t in self.hwnd_title.items():
            if t is not "":
                print(h, t)


if __name__ == "__main__":
    tObj = screenCap()
    screen = tObj.screen()
    print (screen.shape)
    cv2.imwrite('test.png',screen)
    exit()


    tObj.getHwnd()
    tObj.window_capture('haha.bmp')


