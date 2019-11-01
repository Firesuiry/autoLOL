from setting import *
import os
import tensorflow as tf

class modelManager():
    def __init__(self):
        self.path = PROJECT_ADDRESS
        self.models = {}


    def useModel(self, modelName, inputData):
        '''
        使用模型预测值
        :param modelName: 模型名称
        :param inputData: 输入数据
        :return: 预测数据
        '''
        model = self.models.get(modelName, None)
        if model is None:
            model = self.addModel(modelName)
        # print('input',inputData.shape)
        predictions = model.predict(inputData)

        return predictions

    def addModel(self, modelName):
        if not os.path.exists(r'model/{}'.format(modelName)):
            print('模型文件不存在，文件路径：{} 当前路径：{}'.format(r'model/{}'.format(modelName),os.path.abspath(__file__)))
        if self.path is None:
            self.models[modelName] = tf.keras.models.load_model(r'model/{}'.format(modelName))
        else:
            self.models[modelName] = tf.keras.models.load_model(self.path + r'/model/{}'.format(modelName))
        return self.models[modelName]

model_manager = modelManager()