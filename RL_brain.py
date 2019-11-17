import cv2
from modelManger import model_manager
import numpy as np


class policy_gradient:
    def __init__(
            self,
            n_actions,
            n_features,
            learning_rate=0.01,
            reward_decay=0.95,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay

    def determine_action(self, observation):
        """
        通过输入图片决定所需动作 局势检测等在此实现
        :param params:
        :return: 动作字典
        """

        pic = self.currentPic.copy()

        img = cv2.resize(pic, (256, 448))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        feature = model_manager.useModel('encoder.h5', img.reshape(1, 256, 448, 1)).reshape(2048)
        print('feature max:{}'.format(np.max(feature)))
        value_input = np.zeros([3, 2051])
        for i in range(3):
            value_input[i][:2048] = feature
            value_input[i][2048 + i] = 1
        print(value_input[:, 2048:])
        action_value = model_manager.useModel('value_model.h5', value_input).reshape(3)

        action = {
            'go': action_value[0],
            'back': action_value[1],
            'standAndAttack': action_value[2]
        }
        if (action_value == 0).all():
            action['go'] = 5
        print(action)
        return action

