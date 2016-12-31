from PIL import Image
import numpy as np
import os
import edit

def load_image(directory) :
        #add image
        try :
            pillow_image = Image.open(directory)
        except Exception as Import_error :
            raise Exception(Import_error)

        print(pillow_image)    
        width, height = pillow_image.size
        file_size = os.path.getsize(directory)
        info = '{}x{}\n{}\n{} kB'.format(width, height, pillow_image.format, file_size/1000)
        
        #resize if necessary
        pillow_preview_image = scale_both(pillow_image)
        np_image = np.asarray(pillow_image, dtype=np.float)
        #update text
        return pillow_image, pillow_preview_image, np_image, info

def scale_both(pillow_image) :
    pillow_preview_image = pillow_image
    width, height = pillow_image.size

    if width > 1000 :
           pillow_preview_image, width, height = resize(1000, 'WIDTH', pillow_image, pillow_preview_image) 
    if height > 600 :
           pillow_preview_image, width, height = resize(600, 'HEIGHT', pillow_image, pillow_preview_image) 
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
    if mode == 'L' or mode == 'RGB' :
        negativ = edit.inverse(np_image)
    elif mode == 'RGBA' :
        negativ = edit.inverse_RGBA(np_image)
    else :
        return

    negativ_tmp = np.asarray(negativ, dtype=np.uint8)
    print(negativ_tmp.shape, negativ_tmp.size)

    out = Image.fromarray(negativ_tmp, mode)
    out_preview = scale_both(out)

    return out, out_preview, negativ
