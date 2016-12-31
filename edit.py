from PIL import Image
import numpy as np
from numba import jit

def inverse(np_image) :
	negativ = 255 - np_image
	return negativ

def inverse_RGBA(np_image) :
	negativ = np.empty(np_image.shape, dtype=np.float)
	negativ[:,:,0:3] = 255 - np_image[:,:,0:3]
	negativ[:,:,3] = np_image[:,:,3]
	return negativ

@jit
def grayscale(np_image) :
	grayscale = grayscale_core(np_image)
	grayscale = grayscale[:,:,np.newaxis].repeat(3, axis=2) 
	return grayscale

@jit
def grayscale_RGBA(np_image) :
	grayscale = grayscale_core(np_image)
	grayscale = grayscale[:,:,np.newaxis].repeat(4, axis=2) 
	grayscale[:,:,3] = np_image[:,:,3]
	return grayscale

@jit
def grayscale_core(np_image) :
	v_linear = np.vectorize(linear)
	v_gamma = np.vectorize(gamma)
	grayscale = v_linear(np_image[:,:,0:3])
	grayscale = 0.2126 * grayscale[:,:,0] + 0.7152 * grayscale[:,:,1] + 0.0722 * grayscale[:,:,2]
	grayscale = v_gamma(grayscale)
	return grayscale

def linear( C ) :
	if C <= 0.04045 :
		return C / 12.92 
	else :
		return (( C  + 0.055 ) / 1.055) ** 2.4

def gamma( Y ) :
	if Y <= 0.0031308 :
		return 12.92 * Y
	else :
		return 1.055 * (Y ** (1/2.4)) - 0.055

def brightness(np_image, value) :
	i = (value + 100) / 100
	output = np_image * i
	output[output > 255] = 255
	return output

def brightness_RGBA(np_image, value) :
	output = np.empty(np_image.shape, dtype=np.float)
	i = (value + 100) / 100
	output[:,:,0:3] = np_image[:,:,0:3] * i
	output[:,:,3] = np_image[:,:,3]
	output[output > 255] = 255
	return output
