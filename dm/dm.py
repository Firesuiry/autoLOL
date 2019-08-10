import win32com.client
import time
import os,json

class dmBase():
    def __init__(self):
        self.id = 0



    def getCommand(self):
        f_path = r'E:\develop\autoLOL\dm\data\{}.txt'.format(self.id)
        command = ''
        if os.path.exists(f_path):
            with open(f_path) as f:
                command = f.read()
        print(command)
        return command


class dmOperater(dmBase):
    def __init__(self,id,hwnd,manager):

        self.id = id
        self.hwnd = hwnd
        self.manager = manager
        print ('dmOperater启动，id：{} hwnd:{}'.format(id,hwnd))
        self.dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件
        dm_ret = self.dm.SetShowErrorMsg(0)
        dm_ret = self.dm.BindWindowEx(hwnd, "gdi", "windows", "windows", "", 0)
        print('窗口绑定结果：%s'%dm_ret)
        if dm_ret == 0:
            return
        self.commandCahe = ''

        if not os.path.exists('screen'+str(self.id)):
            os.makedirs('screen'+str(self.id))

        self.mainLoop()

    def mainExcuter(self):
        command = self.getCommand()
        dm_ret = self.dm.Capture(0, 0, 2000, 2000, "screen%s/0.bmp" % self.id)
        print ('cap result:{}'.format(dm_ret))
        self.excuteCommand(command)

    def excuteCommand(self,command):
        if command == '' or command == self.commandCahe:
            return
        self.commandCahe == command
        cDict = json.loads(command)

        commandList = cDict['commandList']
        for commandDict in commandList:
            #执行命令模块
            print (commandDict)
            key = commandDict.get('key','')
            x = commandDict.get('x','')
            y = commandDict.get('y', '')
            delay = commandDict.get('delay',100)
            name = commandDict.get('name', '')
            if name == '':
                continue
            mathod = 'self.dm.{}'.format(name)
            args = ''
            for arg in [key,x,y]:
                if arg != '':
                    if args == '':
                        args += '('
                    else:
                        args += ','
                    args += '\'' + str(arg) + '\''
            if args == '':
                args = '()'
            else:
                args += ')'
            command = mathod + args

            try:
                print ('excute command:{}'.format(command))
                eval(command)
                time.sleep(delay/1000)
            except Exception as e:
                print(e)
            finally:
                pass



    def mainLoop(self):
        while True:
            self.mainExcuter()
            time.sleep(0.1)

class dmManager(dmBase):
    def __init__(self):
        self.id = 0
        self.dm = win32com.client.Dispatch('dm.dmsoft')  #调用大漠插件
        print ('dmManager，id：{}'.format(self.id))
        self.operaterHwndsList = []
        self.operaterDict = {}
        self.opId = 0 #为了创建operater储存id
        self.checkHwnd()

    def checkHwnd(self):
        hwnds = self.dm.EnumWindow(0, "League of Legends (TM) Client - [Windows 7 x64]", "", 1 + 4 + 8 + 16)
        print (hwnds)
        print (type(hwnds))
        if type(hwnds) == type('str'):
            hwnds = [hwnds]
        for hwnd in hwnds:
            if hwnd not in self.operaterHwndsList:
                self.opId += 1
                op = dmOperater(self.opId,int(hwnd),self) #此处待开发多线程方式
                opDict = {
                    'id':self.opId,
                    'hwnd':hwnd,
                    'op':op
                }
                self.operaterHwndsList.append(hwnd)
                self.operaterDict[hwnd] = opDict





if __name__ == '__main__':
    p = dmManager()



    exit()
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