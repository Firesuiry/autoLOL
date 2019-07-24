import win32gui

class hwndGetter():
    def __init__(self):
        pass

    def getHwnd(self):
        # 获取主句柄
        classname = "VMUIFrame"
        titlename = "Windows 7 x64 - VMware Workstation"
        self.hwnd = win32gui.FindWindow(classname, titlename)
        print(self.hwnd)
        # 获取所有子句柄
        childHwndList = self.get_child_windows(self.hwnd)
        # 遍历子句柄获取所需
        for hwnd in childHwndList:
            title = win32gui.GetWindowText(hwnd)
            clsname = win32gui.GetClassName(hwnd)
            # print('title:%s clsname:%s'%(title,clsname))
            if 'VMware.GuestWindow' in clsname:
                self.hwnd = hwnd
        print(self.hwnd)

    def get_child_windows(self, parent):
        # 获得parent的所有子窗口句柄
        # 返回子窗口句柄列表
        if not parent:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList

h = hwndGetter()
h.getHwnd()

