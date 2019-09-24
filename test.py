from picProcesser import picProcesser
import cv2

p = picProcesser()
for i in range(10):
	index = i*50+13
	img = cv2.imread(r'E:\develop\autoLOLres\ans\screen{}.bmp'.format(index))
	p.getPic(img)