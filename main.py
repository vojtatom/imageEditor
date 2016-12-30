#!/usr/bin/env python3
 
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import numpy as np
from time import sleep
import os

class Application() :
    def __init__(self, main) :
        self.root = main
        self.root.title("Image editor")
        self.canvas = Canvas(root, width=500, height=200)

        #setup text
        # self.canvas_text = self.canvas.create_text(40, 90, anchor="nw")
        # self.canvas.itemconfig(self.canvas_text, text="click to load the image")
        # self.canvas.bind("<Button-1>", self.image_change)

        self.image_loaded = False

        #menu
        self.menubar = Menu(self.root)

        self.submenu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.submenu1)
        self.submenu1.add_command(label="Load image", command=self.load_image)
        self.submenu1.add_command(label="Save image", command=self.save_image)
        self.submenu1.add_separator()
        self.submenu1.add_command(label="Exit", command=self.exit)

        self.submenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.submenu2)
        self.submenu2.add_command(label="Inverse")
        self.submenu2.add_command(label="Grayscale")
        self.submenu2.add_command(label="Lighten/Darken")
        self.submenu2.add_command(label="Edge Detection")

        self.root.config(menu=self.menubar)
        self.menubar.entryconfig("Edit", state=DISABLED)
        self.submenu1.entryconfig("Save image", state=DISABLED)


        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('PNG', '.png'), ('JPG', '.jpg .jpeg'), ('PPM', '.ppm')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.png'
        options['parent'] = root
        options['title'] = 'Choose file:'

    def add_main_image(self, directory) :
        #remove text
        # self.canvas.delete(self.canvas_text)
        
        #add image
        self.pillow_image = Image.open(directory)
        self.np_image = np.asarray(self.pillow_image, dtype=np.float)
        height, width, dim = self.np_image.shape

        #resize if necessary
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

    def save_main_image(self, directory) :
        self.pillow_image.save(directory)
        self.canvas.delete(self.main_image)
        self.canvas.config(width=500, height=200)
        self.canvas.update()

    def run_application(self) :
        self.canvas.update()
        self.canvas.pack()

    def load_image(self) :
        directory = askopenfile(mode='r', **self.file_opt)
        if directory is None :
            return
        try :
            self.add_main_image(directory.name)
            self.image_loaded = True
            self.menubar.entryconfig("Edit", state=NORMAL)
            self.submenu1.entryconfig("Save image", state=NORMAL)
        except:
            showerror("Opening image", "Can't open this image...")

    def save_image(self) :
        directory = asksaveasfile(mode='w', **self.file_opt)
        if directory is None :
            return
        self.save_main_image(directory.name)
        self.image_loaded = False

    def exit(self) :
        quit()

root = Tk()
root.resizable(width=False, height=False)
app = Application(root)
app.run_application()
root.mainloop()
