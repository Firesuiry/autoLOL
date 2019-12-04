from picProcessor import picProcessor
from operater import operater
from RL_brain import policy_gradient
from setting import *
import time, cv2
from reviewAndTrain.dataStore import dataStore
from enum import Enum
import numpy as np
from train import generate_data_score


class GAME_STATE(Enum):
	LOADING = 0
	RUNNING_INIT = 1
	RUNNING = 2
	ENDING = 3


class agent():
	def __init__(self, agent_id=1, test=False, save_mem=True, init=True):
		self.test = test
		if not test:
			self.operator = operater()
		else:
			self.operator = None
		self.pic_processor = picProcessor(test=False)
		self.id = agent_id
		self.brain = policy_gradient(n_actions=6, n_features=9382)
		if save_mem:
			self.ds = dataStore()
		self.save_mem = save_mem

		self.game_state = GAME_STATE.LOADING
		if not test:
			self.mainLoop(init)

	def end_operate(self):
		print('agent自毁程序已经启动')
		self.pic_processor = None
		self.brain = None

		end_time = time.time() + 30

		# 调用train 开始训练
		try:
			generate_data_score(reCaculateScore=False)
		except Exception as e:
			print('训练出错 错误：',str(e))
			self.ds.err_write(e)

		while time.time() < end_time:
			time.sleep(1)

		self.operator.close()


	def mainLoop(self, init=True, takein_img=None, run_once=False, show_time = False):
		while(True):
			start_time = time.time()
			# ###########################获取ob
			if takein_img is None:
				img = self.operator.get_game_img()
			else:
				img = takein_img

			# ###########################游戏阶段判断
			if self.game_state == GAME_STATE.LOADING:
				print('检测游戏是否加载完成')
				loading_complete = self.pic_processor.loading_complete(img)
				if loading_complete:
					self.game_state = GAME_STATE.RUNNING_INIT
				time.sleep(1)
				continue

			elif self.game_state == GAME_STATE.RUNNING_INIT:
				print('开始进行游戏初始化')
				if TEST_ACTION == -1 and init:
					self.operator.init_action()
				self.game_state = GAME_STATE.RUNNING
				continue

			elif self.game_state == GAME_STATE.RUNNING:
				game_end = self.pic_processor.game_end(img)
				if game_end:
					print('检测到游戏结束 即将进行下一轮检测')
					self.game_state = GAME_STATE.ENDING
					continue

			elif self.game_state == GAME_STATE.ENDING:
				game_end = self.pic_processor.game_end(img) and not self.pic_processor.game_running(img)
				if game_end:
					print('再次检测到游戏结束 即将退出此次进程')
					self.end_operate()
					break
				else:
					print('检测失误 恢复运行状态')
					self.game_state = GAME_STATE.RUNNING
					continue

		# ############################ob加工
			t = time.time()
			try:
				# params = self.pic_processor.param_extract(img, money=False)
				params, obs = self.pic_processor.obs_params_extract(img)
			except Exception as e:
				print(e)
				self.ds.err_write(e)
				time.sleep(1)
				continue
			if show_time:
				print('ob加工所用时间:',time.time()-t)
		# #############################死亡检测与死亡时买装备
			if params['HP'] == 0:
				print('当前已经死亡，执行买装备操作')
				self.operator.auto_buy_equip()
				time.sleep(1)
				continue

		# #############################动作选择
			t = time.time()
			action_prob, action = self.brain.determine_action(obs)
			if TEST_ACTION != -1:  # 测试动作时需要直接调用动作
				action = TEST_ACTION
			if show_time:
				print('动作选择所用时间:',time.time()-t)
		# #############################动作执行
			try:
				params = self.pic_processor.action_params_augment(action, params)
			except Exception as e:
				print(e)
				self.ds.err_write(e)
				time.sleep(1)
				continue
			if not self.test:
				self.operator.actionExcute(action, params)

		# #############################记忆储存
			if self.save_mem:
				self.ds.storeResult(img, params, action,obs,action_prob)

			use_time = time.time() - start_time
			print('完整一轮执行花费时间：', use_time)
			if use_time < 0.5:
				time.sleep(0.5-use_time)

			if run_once:
				break



def loadPic(self, path='res/Screen01.png'):
	pic = cv2.imread(path)
	return pic


TEST_ACTION = -1
if __name__ == "__main__":
	# a = agent(save_mem=False, init=True, test=True)
	# a.game_state = GAME_STATE.RUNNING
	# img =cv2.imread(r'D:\develop\autoLOL\dm\screen1\0.bmp')
	# a.mainLoop(init=False, img=img, run_once=True, show_time=False)
	# # a.mainLoop(init=False, img=img, run_once=True, show_time=True)
	# exit()
	#


	while True:
		print('创建agent等待游戏开启')
		a = agent(save_mem=True, init=True)
		time.sleep(1)
