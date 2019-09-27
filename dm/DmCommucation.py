import socket,select,json
from typing import Any
class DmCommucation:
    """
    大漠插件通过继承这个类，可以使用网络通信调用自身方法
    """
    def start(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """开启链接主处理进程"""
        print("开始链接主进程")
        self.socket.connect(("localhost",4892))
        print("链接成功")
        while True:
            r = select.select([self.socket],[],[])[0]
            data = r[0].recv(2048)
            if data:
                data = self.ParseBag(data)
                ret = self.CallSelfFuc(data["FucName"],data["args"],data["kwargs"])
                self.socket.send(self.BuildBag({"ret":str(ret)}))
            else:
                print("主进程已关闭，自动退出")
                self.socket.close()
                break
    def log(self,s):
        """日志，后续重写"""
        print(s)
    def BuildBag(self,dic:dict) -> bytes:
        """将需要发送的字典转换为数据"""
        return json.dumps(dic).encode()
    def ParseBag(self,data:bytes):
        """收到的数据转换为字典"""
        return json.loads(data.decode())
    def CallSelfFuc(self,FucName:str,args:list,Params:dict) -> Any:
        '''
        :param FucName: 要调用的方法
        :param Parmas: 要调用的方法字典
        :return:返回调用方法的返回值
        '''
        # 参数检查 
        self.log("调用方法：{} 调用参数 {} , {} ".format(FucName,str(args),str(Params)))
        assert isinstance(FucName,str),"FucName must a string"
        assert FucName not in self.__dict__,"invalid FucName"
        fuc = self.__getattr__(FucName)
        try:
            return fuc(*args,**Params)
        except Exception as e:
            return e