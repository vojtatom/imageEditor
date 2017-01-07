from PIL import Image
import numpy as np
from numba import jit
import filters

def inverse(np_image) :
	print(np_image.shape, np_image.size)
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
	output[:,:,] = np_image[:,:,0:3] * i
	output[:,:,3] = np_image[:,:,3]
	output[output > 255] = 255
	return output

def edges_detection(np_image) :
	outputRGB = apply_filter(np_image, filters.edges_detection)
	return outputRGB


def apply_filter(np_image, filter) :
	R, G, B = slice_image(np_image)
	bottom, top = filter_dimensions(filter)
	outR = apply(R, filter, top, bottom)
	outG = apply(G, filter, top, bottom)
	outB = apply(B, filter, top, bottom)
	outRGB = np.dstack((outR, outG, outB))
	return outRGB

def slice_image(np_image) :
	return np_image[:,:,0], np_image[:,:,1], np_image[:,:,2]

def filter_dimensions(effect) :
	bottom = effect[2].shape[0] // 2
	top = bottom + 1
	return bottom, top

@jit
def apply(channel, effect, top, bottom) :
	factor, bias, mask, _ = effect
	height, width = channel.shape
	out = np.zeros(shape=(height - 2 * bottom, width - 2 * bottom))
	
	for y in range(bottom, height - top):
		for x in range(bottom, width - top):
			new_pixel = channel[y - bottom : y + top, x - bottom : x + top]
			tmp = (new_pixel * mask).sum()
			out[y - bottom, x - bottom] = min(abs(int(factor * tmp + bias)), 255);
	return out
