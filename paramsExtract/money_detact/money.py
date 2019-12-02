import numpy as np
import cv2,os

PATH = os.path.split(__file__)[0] + '/'
digit_temple = []
for i in range(10):
	img = cv2.imread(PATH + '{}.png'.format(i),0)
	digit_temple.append(img)

def money_detact(pic: np.ndarray):
	assert pic.shape[2] == 3
	pic = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
	_, pic = cv2.threshold(pic, 200, 255, cv2.THRESH_BINARY)
	pic = np.uint8(pic)/np.max(pic)*255
	return char_split(pic)

def char_split(pic: np.ndarray):
	s = np.sum(pic, axis=0)
	start_id = 0
	money = ''
	for i in range(s.shape[0]):
		if s[i] != 0:
			if start_id == 0:
				start_id = i
		else:
			if start_id != 0:
				char = pic[:,start_id:i]
				money += str(digit_check(char))
				start_id = 0
	return int(money) if money is not '' else 0
chars = []
def add_char(char :np.ndarray):
	global chars
	print('char.shape:',char.shape)
	for c in chars:
		if (c[:,:5] == char[:,:5]).all():
			return
	chars.append(char)

def digit_check(char: np.ndarray):
	new_char = np.zeros((16,8),dtype=np.uint8)
	new_char[:,0:char.shape[1]] = char

	simi = []
	for i in range(10):
		# print(new_char.shape,digit_temple[i].shape,type(new_char[0][0]),type(digit_temple[i][0][0]))
		s = cv2.matchTemplate(new_char,digit_temple[i],cv2.TM_CCOEFF)
		simi.append(np.max(s))
	return np.argmax(simi)


if __name__ == '__main__':
	for i in range(2344):
		img = cv2.imread('E:\err_pic/{}.png'.format(i))
		print(money_detact(img))