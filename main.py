#!/usr/bin/env python3
 
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import numpy as np
from time import sleep
import os
import imageoperations
import edit

class Application() :
    def __init__(self, main) :
        self.root = main
        self.root.title("Image editor")
        self.root.configure(bg='gray7')
        self.canvas = Canvas(root, width=500, height=200, bg='gray7', highlightthickness=0)
        self.loaded = False

        #setup text
        self.canvas_text = self.canvas.create_text(40, 90, anchor="nw", fill='white')
        self.canvas.itemconfig(self.canvas_text, text="Let's start by loading an image...")

        #setup side frame
        self.frame_side = Frame(self.root, bg='gray7', borderwidth=10)

        #setup info label
        self.label1 = Label(self.frame_side, text='Image info:', bg='gray7', fg='white', anchor=W)
        self.label2 = Label(self.frame_side, text='no image', bg='gray7', fg='white', borderwidth=10, anchor=W, justify=LEFT)
        self.label3 = Label(self.frame_side, text='Applied effects:', bg='gray7', fg='white', anchor=W)

        #setup listbox
        self.listbox = Listbox(self.frame_side, relief=FLAT, bg='gray7', fg='white', borderwidth=10, selectborderwidth=0, selectbackground='gray7', selectforeground='white', highlightthickness=0)

        #menu
        self.setup_menu()

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('PNG', '.png'), ('JPG', '.jpg .jpeg'), ('PPM', '.ppm')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.png'
        options['parent'] = root
        options['title'] = 'Choose file:'

    def setup_menu(self) :
        self.menubar = Menu(self.root, bg='gray7', fg='white', relief=FLAT)

        self.submenu1 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="File", menu=self.submenu1)
        self.submenu1.add_command(label="Load image", command=self.load_image)
        self.submenu1.add_command(label="Save image", command=self.save_image)
        self.submenu1.add_separator()
        self.submenu1.add_command(label="Exit", command=self.exit)

        self.submenu2 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Edit", menu=self.submenu2)
        self.submenu2.add_command(label="Inverse", command=self.inverse)
        self.submenu2.add_command(label="Grayscale", command=self.grayscale)
        self.submenu2.add_command(label="Lighten/Darken", command=self.brightness)

        self.submenu3 = Menu(self.menubar, tearoff=0, bg='gray7', fg='white', relief=FLAT)
        self.menubar.add_cascade(label="Filters", menu=self.submenu3)
        self.submenu3.add_command(label="Weak emboss")
        self.submenu3.add_command(label="Strong emboss")
        self.submenu3.add_command(label="Motion emboss")
        self.submenu3.add_command(label="Sharpen - excessive edges")
        self.submenu3.add_command(label="Sharpen - crisp")
        self.submenu3.add_command(label="Sharpen - subtle edges")
        self.submenu3.add_command(label="Edge Detection")

        self.root.config(menu=self.menubar)
        self.menubar.entryconfig("Edit", state=DISABLED)
        self.menubar.entryconfig("Filters", state=DISABLED)
        self.submenu1.entryconfig("Save image", state=DISABLED)

    def menu_enable(self) :
        self.menubar.entryconfig("Edit", state=NORMAL)
        self.submenu1.entryconfig("Save image", state=NORMAL)
        self.menubar.entryconfig("Filters", state=NORMAL)
        self.canvas.delete(self.canvas_text)

    def save_main_image(self, directory) :
        #TODO - apply filters
        self.pillow_image.save(directory)
        self.canvas.update()

    def run_application(self) :
        self.canvas.update()
        self.canvas.pack(side=LEFT)
        self.label1.pack(fill=X)
        self.label2.pack(fill=X)
        self.label3.pack(fill=X)
        self.listbox.pack(expand=1, fill=BOTH)
        self.frame_side.update()
        self.frame_side.pack(expand=1, side=LEFT, fill=BOTH)

    def load_image(self, directory=None) :
        directory = askopenfile(mode='r', **self.file_opt)
        if directory is None :
            return

        try :
            self.load_main_image(directory.name)
            # self.load_main_image(directory)

            if self.loaded == False :
                self.menu_enable()
                self.loaded = True
        except :
            showerror("Opening image", "Can't open this image...")

        self.canvas.update()
        self.frame_side.update()

    def save_image(self) :
        directory = asksaveasfile(mode='w', **self.file_opt)
        if directory is None :
            return
        self.save_main_image(directory.name)
        self.image_loaded = False

    def load_main_image(self, directory) :
        #add image and info
        self.pillow_image, self.pillow_preview_image, self.np_image, info = imageoperations.load_image(directory)
        width, height = self.pillow_preview_image.size
        self.mode = self.pillow_image.mode
        self.data = ImageTk.PhotoImage(self.pillow_preview_image) 
        self.main_image = self.canvas.create_image((width, height), image=self.data, anchor=SE)
        self.canvas.config(width=width, height=height, bg='white')
        self.label2.config(text=info)
        self.listbox.delete(0, END)

    def exit(self) :
        quit()

    #APPLYING FILTERS
    def inverse(self) :
        self.pillow_image, self.pillow_preview_image, self.np_image = imageoperations.inverse(self.np_image, self.mode)
        self.update_app("inverse")

    def grayscale(self) :
        self.pillow_image, self.pillow_preview_image, self.np_image = imageoperations.grayscale(self.np_image, self.mode)
        self.update_app("grayscale")

    def brightness(self) :
        #setup preview
        self.br_window = Toplevel(bg='gray7')
        self.br_window.title("Brightness")
        self.br_window.resizable(width=False, height=False)
        self.br_frame = Frame(self.br_window, bg='gray7', borderwidth=10)

        self.slider = Scale(self.br_window, from_=-100, to=400, bg='gray7', fg='white', troughcolor='gray7', orient=HORIZONTAL, highlightthickness=0)
        self.apply_button = Button(self.br_frame, text="Apply", bg='gray7', fg='white', command=self.apply_brightness, highlightthickness=0)
        self.preview_button = Button(self.br_frame, text="Preview", bg='gray7', fg='white', command=self.apply_preview, highlightthickness=0)

        #adjust preview
        self.br_preview, self.br_np_image = imageoperations.get_miniature(self.pillow_image)
        self.br_np_original = self.br_np_image
        width, height = self.br_preview.size
        self.br_canvas = Canvas(self.br_window, width=width, height=height, bg='white', highlightthickness=0)
        self.br_data = ImageTk.PhotoImage(self.br_preview) 
        self.br_preview_image = self.br_canvas.create_image((width, height), image=self.br_data, anchor=SE)

        self.br_canvas.pack(fill=BOTH)
        self.slider.pack(fill=BOTH)
        self.preview_button.pack(side=LEFT)
        self.apply_button.pack(side=LEFT)
        self.br_frame.update()
        self.br_frame.pack(expand=1, fill=BOTH)

    def update_app(self, value) :
        self.data = ImageTk.PhotoImage(self.pillow_preview_image)
        self.listbox.insert(END, value) 
        self.canvas.itemconfig(self.main_image, image=self.data)
        self.canvas.update()
        self.frame_side.update()

    def apply_preview(self) :
        value = self.slider.get()
        self.br_preview, _, self.br_np_image = imageoperations.brightness(self.br_np_original, self.mode, value)
        self.br_data = ImageTk.PhotoImage(self.br_preview) 
        self.br_canvas.itemconfig(self.br_preview_image, image=self.br_data)
        self.br_canvas.update()

    def apply_brightness(self) :
        value = self.slider.get()
        self.br_window.destroy()
        self.pillow_image, self.pillow_preview_image, self.np_image = imageoperations.brightness(self.np_image, self.mode, value)
        self.update_app("brightness")

root = Tk()
# turend off doesn't work sometimes ---
root.resizable(width=False, height=False)
app = Application(root)
app.run_application()
# app.load_image('./bird.png')
# app.load_image('./kvetina.ppm')
# app.load_image('./rgba.png')
# app.load_image('./channel1.png')
root.mainloop()
