from PIL import Image
import numpy as np
import os
import edit
import filters

def load_image(directory) :
        #add image
        try :
            pillow_image = Image.open(directory)
        except Exception as Import_error :
            raise Exception(Import_error)
  
        width, height = pillow_image.size
        file_size = os.path.getsize(directory)
        info = create_info(width, height, pillow_image.format, file_size)
        
        #resize if necessary
        pillow_preview_image = scale_both(pillow_image)
        np_image = np.asarray(pillow_image, dtype=np.float)
        #update text
        return pillow_image, pillow_preview_image, np_image, info, (width, height, pillow_image.format, file_size)

def update_image(pillow_image, info) :
    #resize if necessary
    pillow_preview_image = scale_both(pillow_image)
    np_image = np.asarray(pillow_image, dtype=np.float)

    #update text
    return pillow_image, pillow_preview_image, np_image


def update_size_info(pillow_image, info) :
    width, height = pillow_image.size
    return create_info(width, height, info[2], info[3]), (width, height, info[2], info[3])

def create_info(width=0, height=0, format=0, size=0) : 
        info = '{}x{}\n{}\n{} kB'.format(width, height, format, size/1000)
        return info

def get_miniature(pillow_image) :
    out_preview = scale_both(pillow_image, 300, 300)
    np_image = np.asarray(out_preview, dtype=np.float)
    return out_preview, np_image

def scale_both(pillow_image, w_max = 1000, h_max = 600) :
    pillow_preview_image = pillow_image
    width, height = pillow_image.size

    if width > w_max :
           pillow_preview_image, width, height = resize(w_max, 'WIDTH', pillow_image, pillow_preview_image) 
    if height > h_max :
           pillow_preview_image, width, height = resize(h_max, 'HEIGHT', pillow_image, pillow_preview_image) 
    return pillow_preview_image

def resize(base, orientation, pillow_image, pillow_preview_image) :
    if orientation == 'WIDTH' :
        x, y = pillow_preview_image.size
    else :
        y, x = pillow_preview_image.size
    wpercent = base / x
    new_size = int(y * wpercent)
    if orientation == 'WIDTH' :
        pillow_preview_image = pillow_image.resize((base, new_size), Image.ANTIALIAS)
        return pillow_preview_image, base, new_size
    else :
        pillow_preview_image = pillow_image.resize((new_size, base), Image.ANTIALIAS)
        return pillow_preview_image, new_size, base
        
def inverse(np_image, mode) :
    if mode == 'L' or mode == 'RGB' or mode =='P' :
        negativ = edit.inverse(np_image)
    elif mode == 'RGBA' :
        negativ = edit.inverse_RGBA(np_image)
    else :
        return #NOT SUPPORTED

    return output(negativ, mode)

def grayscale(np_image, mode) :
    if mode == 'RGB' :
        grayscale = edit.grayscale(np_image)
    elif mode == 'RGBA' :
        grayscale = edit.grayscale_RGBA(np_image)
    else :
        return #NOT SUPPORTED

    return output(grayscale, mode)

def brightness(np_image, mode, value) :
    if mode == 'L' or mode == 'RGB' or mode =='P' :
        brightness = edit.brightness(np_image, value)
    elif mode == 'RGBA' :
        brightness = edit.brightness_RGBA(np_image, value)
    else :
        return #NOT SUPPORTED

    return output(brightness, mode)

def output(np_image, mode) :
    np_tmp = np.asarray(np_image, dtype=np.uint8)
    out = Image.fromarray(np_tmp, mode)
    out_preview = scale_both(out)

    return out, out_preview, np_image

def edges_detection(np_image, mode) :
    out = edit.filter(filters.edges_detection, np_image, mode)
    return output(out, mode)

def emboss_weak(np_image, mode) :
    out = edit.filter(filters.emboss_weak, np_image, mode)
    return output(out, mode)

def emboss_strong(np_image, mode) :
    out = edit.filter(filters.emboss_strong, np_image, mode)
    return output(out, mode)

def motion_blur(np_image, mode) :
    out = edit.filter(filters.motion_blur, np_image, mode)
    return output(out, mode)

def sharpen_ee(np_image, mode) :
    out = edit.filter(filters.sharpen_ee, np_image, mode)
    return output(out, mode)

def sharpen_c(np_image, mode) :
    out = edit.filter(filters.sharpen_c, np_image, mode)
    return output(out, mode)

def sharpen_se(np_image, mode) :
    out = edit.filter(filters.sharpen_se, np_image, mode)
    return output(out, mode)

