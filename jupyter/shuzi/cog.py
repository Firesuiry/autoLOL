import numpy as np
import cv2
from skimage import morphology
from sklearn.cluster import MeanShift
import time
from PIL import Image
import matplotlib.pyplot as plt


i = 0
while True:
	pic = cv2.imread(r'{}.png'.format(i))
	if pic is None:
		break


	plt.imshow(pic)
	plt.show()
	a = input("input:")




	i += 1