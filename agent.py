from picProcessor import picProcessor
from operater import operater
from RL_brain import policy_gradient
from setting import *
import time, cv2
from reviewAndTrain.dataStore import dataStore
from enum import Enum


class GAME_STATE(Enum):
	LOADING = 0
	RUNNING_INIT = 1
	RUNNING = 2
	ENDING = 3


class agent():
	def __init__(self, agent_id=1, test=False, save_mem=True):
		if not test:
			self.operator = operater()
		else:
			self.operator = None
		self.pic_processor = picProcessor(test=False)
		self.id = agent_id
		self.brain = policy_gradient(0, 0)
		if save_mem:
			self.ds = dataStore()
		self.save_mem = save_mem

		self.game_state = GAME_STATE.LOADING
		if not test:
			self.mainLoop()
			self.operator

	def mainLoop(self):
		while (True):
			# ###########################获取ob
			img = self.operator.get_game_img()

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
				if TEST_ACTION == -1:
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
					delay_shutdown_time = 30
					for i in range(delay_shutdown_time):
						time.sleep(1)
						print(delay_shutdown_time-i)
					self.operator.close()
					break
				else:
					print('检测失误 恢复运行状态')
					self.game_state = GAME_STATE.RUNNING
					continue

		# ############################ob加工
			try:
				params = self.pic_processor.param_extract(img, money=False)
			except Exception as e:
				print(e)
				time.sleep(1)
				continue

		# #############################动作选择
			action = self.brain.determine_action(params)
			if TEST_ACTION != -1:  # 测试动作时需要直接调用动作
				action = TEST_ACTION

		# #############################动作执行
			self.operator.actionExcute(action, params)

		# #############################记忆储存
			if self.save_mem:
				self.ds.storeResult(img, params, action)

			time.sleep(1)


def loadPic(self, path='res/Screen01.png'):
	pic = cv2.imread(path)
	return pic


if __name__ == "__main__":
	TEST_ACTION = -1
	while True:
		print('创建agent等待游戏开启')
		a = agent(save_mem=False)
		time.sleep(1)
