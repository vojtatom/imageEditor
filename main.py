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
        self.listbox.insert(END, "no filters")

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
        self.submenu2.add_command(label="Inverse")
        self.submenu2.add_command(label="Grayscale")
        self.submenu2.add_command(label="Lighten/Darken")

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

    def load_image(self) :
        directory = askopenfile(mode='r', **self.file_opt)
        if directory is None :
            return
        try :
            self.load_main_image(directory.name)
            self.image_loaded = True

            if self.loaded == False :
                self.menu_enable()
                self.loaded = True

        except ValueError :
            print(ValueError)
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
        #add image
        self.pillow_image = Image.open(directory)
        print(self.pillow_image)
        self.np_image = np.asarray(self.pillow_image, dtype=np.float)    
        width, height = self.pillow_image.size
        file_size = os.path.getsize(directory)
        self.pillow_preview_image = self.pillow_image

        #resize if necessary
        if width > 1000 :
           width, height = self.resize(1000, 'WIDTH') 
        if height > 600 :
            width, height = self.resize(600, 'HEIGHT') 

        self.data = ImageTk.PhotoImage(self.pillow_preview_image) 
        self.main_image = self.canvas.create_image((width, height), image=self.data, anchor=SE)
        self.canvas.config(width=width, height=height)
        
        #update text
        info = '{}x{}\n{}\n{} kB'.format(width, height, self.pillow_image.format, file_size/1000)
        self.label2.config(text=info)

    def resize(self, base, orientation) :
        if orientation == 'WIDTH' :
            x, y = self.pillow_preview_image.size
        else :
            y, x = self.pillow_preview_image.size
        wpercent = base / x
        new_size = int(y * wpercent)
        if orientation == 'WIDTH' :
            self.pillow_preview_image = self.pillow_image.resize((base, new_size), Image.ANTIALIAS)
            return base, new_size
        else :
            self.pillow_preview_image = self.pillow_image.resize((new_size, base), Image.ANTIALIAS)
            return new_size, base
            
    def exit(self) :
        quit()

root = Tk()
# turend off doesn't work ---
root.resizable(width=False, height=False)
app = Application(root)
app.run_application()
root.mainloop()
