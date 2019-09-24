import numpy as np
import cv2
from typing import Any
import tensorflow as tf


def RemoveZero(det: np.array) -> np.array:
	"""去除上下的空元素"""
	h, w = det.shape[:2]
	need_del = []
	for i in range(h):
		if np.all(det[i, :] == 0):
			need_del.append(i)
	det = np.delete(det, need_del, axis=0)
	return det


def get_charter(self:Any,pic: np.array) -> int:
	"""通过取阈值来得到的二值化图像，再通过是否存在像素点来分割图像"""
	"""返回值:分割图像的numpy数组"""
	img = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
	_, det = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
	det = RemoveZero(det)
	pre_value = True
	need_slice = []
	h, w = det.shape[:2]
	for i in range(w):
		if pre_value != np.all(det[:, i] == 0):
			pre_value = np.all(det[:, i] == 0)
			need_slice.append(i)
	ret = []
	while need_slice:
		k = need_slice.pop(0)
		e = need_slice.pop(0)
		done_array = det[:, k:e]
		w_add, h_add = 12 - done_array.shape[0], 7 - done_array.shape[1]
		ret.append(np.pad(done_array, ((w_add, 0), (0, h_add)), "constant", constant_values=(0, 0)))
	ll = np.argmax(self.ai.useModel("Money.h5", np.array(ret)), axis=1).tolist()
	p = ""
	for i in ll:
		p += str(i)
	return int(p)
if __name__ == '__main__':
	model = tf.keras.models.load_model(r'C:\Users\Administrator\Desktop\vr\autoLOL\autoLOL\model\Money.h5')
	pic = cv2.imread(r"C:\Users\Administrator\Desktop\ans\MONEY10.png")
	test_images = get_charter(pic)
	print(test_images)
