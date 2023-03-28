#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
from PIL import ImageTk,Image  
import os
import time

# from  control_frame import Control_interface
# from  setup_frame   import Setup_interface

os.system('xset r off')


class Image_frame():
        
    def create_image_frame(self,root,img_name):
        image = Image.open(img_name)
        image = image.resize((800, 600))
        self.img = ImageTk.PhotoImage(image)
        image_frame = tk.Frame(root, width=800, height=600)
        self.canvas = tk.Canvas(image_frame, width=800, height=600, bg='white',)
        self.canvas.pack(fill='both',expand = True)
        self.img_id=self.canvas.create_image(400,300,image=self.img)
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        ttk.Button(image_frame, text='Pause', command=lambda: self.reload_image(root)).pack()
        image_frame.grid(column=0, row=1)
        ttk.Button(image_frame, text='Continue', command=lambda: self.reload_image(root)).pack()
        image_frame.grid(column=1, row=1)
        ttk.Button(image_frame, text='Next', command=lambda: self.reload_image(root)).pack()
        image_frame.grid(column=2, row=1)

    def reload_image(self,root):
        self.canvas.destroy()
        self.create_image_frame(root,'./Figure_1.jpg')



def create_main_window():
    root = tk.Tk()
    root.title('Monitor interface SETAV-2')
    root.resizable(0, 0)

    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    
    image_frame_obj = Image_frame()
    image_frame_obj.create_image_frame(root,'./Figure_1.jpg')

    root.mainloop()

if __name__ == "__main__":
    create_main_window()