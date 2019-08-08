import time

import json,os

class operater():
    def __init__(self,id = 0):
        self.id = id
        self.commandCahe = {
            'time':0,
            'commandList':[]
        }

    def sendCommand(self):
        f_path = r'E:\develop\autoLOL\dm\data\{}.txt'.format(self.id)
        self.commandCahe['time'] = time.time()
        command = json.dumps(self.commandCahe)
        self.commandCahe = {
            'time':0,
            'commandList':[]
        }
        with open(f_path,'w') as f:
            command = f.write(command)



    def addKeyboardCommandToJson(self,keyChar,delay = 100,Down = False,Up = False):
        mathodName = 'KeyPressChar'
        if Down:
            mathodName = 'KeyDownChar'
        if Up:
            mathodName = 'KeyUpChar'

        print('addKeyboardCommandToJson mathod:{} key:{} delay={}'.format(mathodName,keyChar,delay))
        command = {
            'name':mathodName,
            'key':keyChar,
            'delay':delay
        }
        self.commandCahe['commandList'].append(command)


    def addMouseCommandToJson(self,x = -1,y = -1,liftClick = False,rightClick = False,delay = 100):
        '''
        :param x: -1==NoMove
        :param y: -1==NoMove
        :param liftClick:
        :param rightClick:
        :param delay:
        :return:
        '''
        if x != -1 and y != -1:
            mathodName = 'MoveTo'
            command = {
                'name':mathodName,
                'x':x,
                'y':y,
                'delay':delay
            }
            self.commandCahe['commandList'].append(command)

        mathodName = ''
        if liftClick:
            mathodName = 'LeftClick'
        if rightClick:
            mathodName = 'RightClick'
        if mathodName == '':
            return
        command = {
            'name':mathodName,
            'delay':delay
        }
        self.commandCahe['commandList'].append(command)






if __name__ == "__main__":
    p = operater(1024)
    p.addKeyboardCommandToJson('ctrl',Down=True)
    p.addKeyboardCommandToJson('w')
    p.addKeyboardCommandToJson('ctrl',Up=True)
    p.addMouseCommandToJson(1000,1000,liftClick=True)
    p.sendCommand()



