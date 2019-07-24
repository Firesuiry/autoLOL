import win32com.client
import time


dm = win32com.client.Dispatch('dm.dmsoft')  #调用大漠插件
print(dm.ver())#输出版本号
hwnds = dm.EnumWindow(0,"League of Legends (TM) Client - [Windows 7 x64]","",1+4+8+16)
print(hwnds)
hwnd = int(hwnds)

dm_ret = dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
print('结果：%s'%dm_ret)
start = time.time()
last = 0
i = 0
while True:
    if time.time() - last > 0.5:
        i += 1
        dm_ret = dm.Capture(0,0,2000,2000,"ans/screen%s.bmp"%i)
        print('第%s张 结果：%s'%(i,dm_ret))
        last = time.time()
print('经过的时间：%s'%(time.time()-start))

dm_ret = dm.UnBindWindow()
print('结果：%s'%dm_ret)