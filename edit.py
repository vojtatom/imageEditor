from PIL import Image
import numpy as np
from numba import jit

@jit
def inverse(np_image) :
	negativ = 255 - np_image
	return negativ

@jit
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

@jit
def brightness(np_image, value) :
	i = (value + 100) / 100
	output = np_image * i
	output[output > 255] = 255
	return output

@jit
def brightness_RGBA(np_image, value) :
	output = np.empty(np_image.shape, dtype=np.float)
	i = (value + 100) / 100
	output[:,:,0:3] = np_image[:,:,0:3] * i
	output[:,:,3] = np_image[:,:,3]
	output[output > 255] = 255
	return output

def filter(filter, np_image, mode) :
	if mode == 'L' or mode == 'P':
		output = apply_filter_L(np_image, filter)
	elif mode == 'RGB' :
		output = apply_filter_RGB(np_image, filter)
	elif mode == 'RGBA' :
		output = apply_filter_RGB(np_image, filter)
		output = apply_alpha(output, np_image, filter)
	return output

@jit
def apply_filter_RGB(np_image, filter) :
	R, G, B = np_image[:,:,0], np_image[:,:,1], np_image[:,:,2]
	bottom, top = filter_dimensions(filter)
	outR = apply(R, filter, top, bottom)
	outG = apply(G, filter, top, bottom)
	outB = apply(B, filter, top, bottom)
	outRGB = np.dstack((outR, outG, outB))
	return outRGB

@jit
def apply_filter_L(np_image, filter) :
	bottom, top = filter_dimensions(filter)
	out = apply(np_image, filter, top, bottom)
	return out

@jit
def apply_alpha(outputRGBA, np_image, filter) :
	bottom, top = filter_dimensions(filter)
	alpha = np_image[bottom:-bottom,bottom:-bottom,np.newaxis,3]
	RGBA = np.concatenate((outputRGBA, alpha), axis=2)
	return RGBA

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
