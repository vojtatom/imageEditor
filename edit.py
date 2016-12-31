from PIL import Image
import numpy as np

def inverse(np_image):
	print(np_image.shape, np_image.size)
	negativ = 255 - np_image
	return negativ

def inverse_RGBA(np_image):
	negativ = np.empty(np_image.shape, dtype=np.float)
	negativ[:,:,0:3] = 255 - np_image[:,:,0:3]
	negativ[:,:,3] = np_image[:,:,3]
	return negativ