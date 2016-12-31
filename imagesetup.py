from PIL import Image
import numpy as np
import os

def load_image(directory) :
        #add image
        try :
            pillow_image = Image.open(directory)
        except Exception as Import_error :
            raise Exception(Import_error)

        print(pillow_image)
        np_image = np.asarray(pillow_image, dtype=np.float)    
        width, height = pillow_image.size
        file_size = os.path.getsize(directory)
        pillow_preview_image = pillow_image
        info = '{}x{}\n{}\n{} kB'.format(width, height, pillow_image.format, file_size/1000)

        #resize if necessary
        if width > 1000 :
           pillow_preview_image, width, height = resize(1000, 'WIDTH', pillow_image, pillow_preview_image) 
        if height > 600 :
           pillow_preview_image, width, height = resize(600, 'HEIGHT', pillow_image, pillow_preview_image) 

        
        #update text
        return pillow_image, pillow_preview_image, np_image, info

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
        