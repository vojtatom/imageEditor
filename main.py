#!/usr/bin/env python3
 
from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import numpy as np
from time import sleep

class Application() :
    def __init__(self, main) :
        self.root = main
        self.canvas = Canvas(root, width=500, height=200)

        #setup text
        self.canvas_text = self.canvas.create_text(40, 90, anchor="nw")
        self.canvas.itemconfig(self.canvas_text, text="this is the text")
        self.canvas.bind("<Button-1>", self.canvas_click)

        self.image_loaded = False

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.png'
        options['parent'] = root
        options['title'] = 'Choose file:'

    def add_main_image(self, directory) :
        #remove text
        self.canvas.delete(self.canvas_text)
        
        #add image
        self.pillow_image = Image.open(directory)
        self.np_image = np.asarray(self.pillow_image, dtype=np.float)
        height, width, dim = self.np_image.shape

        if width > 1000 :
            basewidth = 1000
            wpercent = basewidth / width
            hsize = int(height * wpercent)
            self.pillow_preview_image = self.pillow_image.resize((basewidth, hsize), Image.ANTIALIAS)
        else :
            self.pillow_preview_image = self.pillow_image

        self.data = ImageTk.PhotoImage(self.pillow_preview_image) 
        width, height = self.data.width(), self.data.height()
        self.main_image = self.canvas.create_image((width, height), image=self.data, anchor=SE)
        self.canvas.config(width=width, height=height)
        self.canvas.update()

    def run_application(self) :
        self.canvas.update()
        self.canvas.pack()

    def canvas_click(self, event) :
        if self.image_loaded == False :
            directory = ask_open(self.file_opt)
            print(directory)
            self.add_main_image(directory.name)
            self.image_loaded = True


def ask_open(file_opt) :
    return askopenfile(mode='r', **file_opt)

root = Tk()
root.resizable(width=False, height=False)
app = Application(root)
app.run_application()
root.mainloop()
