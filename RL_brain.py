import cv2
from modelManger import model_manager
import numpy as np
import random


class policy_gradient:
    def __init__(
            self,
            n_actions=0,
            n_features=0,
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
        if observation['HP'] < 0.5:
            return 0

        actions = [0,1,2,3]
        action = random.choices(actions, [0.05, 0.5, 0.25, 0.25])[0]
        return action

