import cv2
import numpy as np
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense
import os
from setting import *


class policy_gradient:
	def __init__(
			self,
			n_actions=0,
			n_features=0,
			learning_rate=0.01,
			reward_decay=0.95,
	):
		assert n_actions != 0 and n_features != 0
		self.n_actions = n_actions
		self.n_features = n_features
		self.lr = learning_rate
		self.gamma = reward_decay
		self.net_learning_rate = 0.005
		self.creat_net(self.n_features, self.n_actions)

	def determine_action(self, observation):
		"""
		通过输入图片决定所需动作 局势检测等在此实现
		:param params:
		:return: 动作字典
		"""
		action_prob = self.actor_evaluate_net.predict(observation[np.newaxis])[0]
		actions = [0,1,2,3,4,5]
		action = random.choices(actions, action_prob)
		return action

	def creat_net(self, state_dims: int, action_dims: int):
		path = PROJECT_ADDRESS + 'model/a0.h5'
		if os.path.exists(path):
			self.actor_evaluate_net = keras.models.load_model(path)
		else:
			self.actor_evaluate_net = self.bulid_actor_net(state_dims, action_dims)

		path = PROJECT_ADDRESS + 'model/a1.h5'
		if os.path.exists(path):
			self.actor_target_net = keras.models.load_model(path)
		else:
			self.actor_target_net = self.bulid_actor_net(state_dims, action_dims)

		path = PROJECT_ADDRESS + 'model/c0.h5'
		if os.path.exists(path):
			self.critic_evaluate_net = keras.models.load_model(path)
		else:
			self.critic_evaluate_net = self.bulid_critic_net(state_dims, action_dims)

		path = PROJECT_ADDRESS + 'model/c1.h5'
		if os.path.exists(path):
			self.critic_target_net = keras.models.load_model(path)
		else:
			self.critic_target_net = self.bulid_critic_net(state_dims, action_dims)

	def save_net(self):
		path = PROJECT_ADDRESS + 'model/a0.h5'
		self.actor_evaluate_net.save(path)

		path = PROJECT_ADDRESS + 'model/a1.h5'
		self.actor_target_net.save(path)

		path = PROJECT_ADDRESS + 'model/c0.h5'
		self.critic_evaluate_net.save(path)

		path = PROJECT_ADDRESS + 'model/c1.h5'
		self.critic_target_net.save(path)

	def bulid_actor_net(self, state_dims: int, action_dims: int):
		state_input = keras.Input(shape=(state_dims), name='state')
		x = Dense(128)(state_input)
		x = Dense(32)(x)
		action_output = Dense(action_dims, activation='softmax')(x)
		model = keras.Model(state_input, action_output)
		return model

	def bulid_critic_net(self, state_dims: int, action_dims: int):
		state_action_input = keras.Input(shape=(state_dims + action_dims), name='state')
		x = Dense(128)(state_action_input)
		x = Dense(32)(x)
		value = Dense(1)(x)
		model = keras.Model(state_action_input, value)
		return model

	def learn(self, observations, actions, rewards, next_observations):
		# 训练执行者网络
		observation_tensor = tf.convert_to_tensor(observations, dtype=tf.float32)
		with tf.GradientTape() as tape:
			action_tensor = self.actor_evaluate_net(observation_tensor)
			action_tensor = tf.math.argmax(action_tensor)
			one_hot_action_tensor = tf.one_hot(action_tensor, self.n_actions)
			input_tensor = tf.concat([observation_tensor,one_hot_action_tensor], axis=1)
			q_tensor = self.critic_evaluate_net(input_tensor)
			loss_tensor = -tf.math.reduce_mean(q_tensor)
		grad_tensors = tape.gradient(loss_tensor,
		                             self.actor_evaluate_net.variables)
		self.actor_evaluate_net.optimizer.apply_gradients(zip(
			grad_tensors, self.actor_evaluate_net.variables))

		# 训练评论者网络
		next_actions = self.actor_target_net.predict(
			next_observations)
		assert next_actions.shape[1] == self.n_actions
		next_actions_one_hot = np.float(next_actions == np.max(next_actions))
		observation_actions = np.hstack([observations, next_actions_one_hot])
		next_observation_actions = np.hstack(
			[next_observations, next_actions])
		next_qs = self.critic_target_net.predict(
			next_observation_actions)[:, 0]
		targets = rewards + self.gamma * next_qs
		self.critic_evaluate_net.fit(observation_actions, targets, verbose=0)

		self.update_target_net(self.actor_target_net,
		                       self.actor_evaluate_net, self.net_learning_rate)
		self.update_target_net(self.critic_target_net,
		                       self.critic_evaluate_net, self.net_learning_rate)

	def update_target_net(self, target_net, evaluate_net, learning_rate=1.):
		target_weights = target_net.get_weights()
		evaluate_weights = evaluate_net.get_weights()
		average_weights = [(1. - learning_rate) * t + learning_rate * e
		                   for t, e in zip(target_weights, evaluate_weights)]
		target_net.set_weights(average_weights)


	# 回家0
	# 前进1
	# 后退2
	# 原地A3
	# 走到己方小兵的中心位置4
	# 攻击最近的敌方小兵5

if __name__ == '__main__':
	brain = policy_gradient()
