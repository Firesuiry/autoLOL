import socket,select,json
class MainCommucation:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.con = None
    def start(self):
        """开始等待大漠通信链接"""
        print("等待大漠模块链接")
        self.socket.bind(("",4892))
        self.socket.listen(1)
        self.con,addr = self.socket.accept()
        print("链接成功，来自:{}".format(str(addr)))
        self.socket.close()
    def __getattr__(self, item):
        def dock(*args,**kwargs):
            if self.con:
                self.con.send(self.BuildBag({
                    "FucName":item,
                    "args":args,
                    "kwargs":kwargs,
                }))
                r = select.select([self.con],[],[],1)[0]
                if not r:
                    raise TimeoutError("等待回应超时！")
                else:
                    return self.ParseBag(r[0].recv(1024))["ret"]
        return dock if item not in self.__dict__ else getattr(self,item)
    def BuildBag(self,dic:dict) -> bytes:
        """将需要发送的字典转换为数据"""
        return json.dumps(dic).encode()
    def ParseBag(self,data):
        """收到的数据转换为字典"""
        return json.loads(data.decode())
if __name__ == '__main__':
    w = MainCommucation()
    import time
    # 先开启主进程的通讯，等待大漠链接
    w.start()
    time.sleep(2)
    ss = time.time()
    print(w.MoveTo(123, 321))
    print(w.RightClick())
    print(time.time() - ss)