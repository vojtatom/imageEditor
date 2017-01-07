import numpy as np

emboss_strong = (1, 128, np.array([
	[-1, -1, -1, -1, 0],
	[-1, -1, -1,  0, 1],
	[-1, -1,  0,  1, 1],
	[-1,  0,  1,  1, 1],
	[ 0,  1,  1,  1, 1]]),
	"emboss strong")

# emboss weak
emboss_weak = (1, 128, np.array([
	[ -1, -1, 0],
	[ -1,  0, 1],
	[  0,  1, 1]]),
	"emboss weak")

# motion blur
motion_blur = (1 / 9, 0, np.array([
	[1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 1]]),
	"motion blur")

# edge detection
edges_detection = (1, 0, np.array([
	[ -1, -1, -1],
	[ -1,  8, -1],
	[ -1, -1, -1]]),
	"edges detection")

# sharpen - edges excessively
sharpen_ee = (1, 0, np.array([
	[ 1,  1, 1],
	[ 1, -7, 1],
	[ 1,  1, 1]]),
	"sharpen - edges excessively")

# sharpen - subtle edges
sharpen_se = (1 / 8, 0, np.array([
	[ -1, -1, -1, -1, -1 ],
	[ -1,  2,  2,  2, -1 ],
	[ -1,  2,  8,  2, -1 ],
	[ -1,  2,  2,  2, -1 ],
	[ -1, -1, -1, -1, -1 ]]),
	"sharpen - subtle edges")

# sharpen - crisp
sharpen_c = (1, 0, np.array([
	[ -1, -1, -1],
	[ -1,  9, -1],
	[ -1, -1, -1]]),
	"sharpen - crisp")

filters = (emboss_strong, emboss_weak, motion_blur, edges_detection, sharpen_ee, sharpen_se, sharpen_c)