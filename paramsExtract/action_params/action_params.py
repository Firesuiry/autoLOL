import numpy as np
import cv2

def get_target_action(mat):
	print(mat.shape)
	assert mat.shape == (1, 3, 22, 40)
	center_of_ally = [-1, -1]
	nearest_enemy = [-1, -1]
	ally_soldier_mat = mat[0][0]
	enemy_soldier_mat = mat[0][1]

	# 计算我方小兵中点
	ally_poss = np.array(np.where(ally_soldier_mat>0.5))
	assert ally_poss.shape[0] == 2
	if ally_poss.shape[1] > 0:
		y = np.mean(ally_poss[0])*32+16
		x = np.mean(ally_poss[1])*32+16
		center_of_ally = [int(x),int(y)]

	# 计算敌方最近小兵位置
	enemy_poss = np.array(np.where(enemy_soldier_mat>0.5))
	if enemy_poss.shape[1] > 0:
		new_poss = np.square(enemy_poss - np.array([[11],[20]]))
		dists = np.sum(new_poss, axis=0)
		assert len(dists.shape) == 1, (dists.shape,len(dists.shape))
		min_index = np.argmin(dists)
		assert enemy_poss.shape[0] == 2,enemy_poss
		y = enemy_poss[0][min_index]
		x = enemy_poss[1][min_index]
		y = int(y*32+16)
		x = int(x*32+16)
		nearest_enemy = [x, y]

	return center_of_ally, nearest_enemy



if __name__ == '__main__':
	pass
