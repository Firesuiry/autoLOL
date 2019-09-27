import win32com.client
import time
import DmCommucation as dc
import time
class hh(dc.DmCommucation):
    def __init__(self):
        #调用大漠插件
        self.dm = win32com.client.Dispatch('dm.dmsoft')  
        self.ver = self.dm.ver()
        # 需要绑定窗口的名称
        self.BindWindowName = "百度一下，你就知道"
        hwnd = self.dm.EnumWindow(0,self.BindWindowName,"",1+4+8+16)
        self.bind_ret = "失败"
        if hwnd:
            self.bind_ret = "成功" if self.dm.BindWindowEx(int(hwnd), "gdi", "windows", "windows", "", 0) == 1 else "失败"
        self.log("[{}] 绑定{}".format(self.BindWindowName,self.bind_ret))
    def jietu(self,picname):
        return self.dm.Capture(0,0,2000,2000,r"C:\\Users\\Administrator\\Desktop\\" + str(picname))
    def __getattr__(self,item):
        def dock(*args,**kwargs):
            if self.bind_ret == "失败":return "大漠未绑定窗口"
            return getattr(self.dm,item)(*args,**kwargs)
        return dock if item not in self.__dict__ else getattr(self,item)
if __name__ == '__main__':
    ww = hh()
    ww.start()