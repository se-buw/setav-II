#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
import os

from  control_frame import Control_frame
from  setup_frame   import Setup_frame

os.system('xset r off')



def create_main_window():
    root = tk.Tk()
    root.title('Replace')
    root.resizable(0, 0)

    # add Key capture
    root.bind('<KeyPress>', Control_frame().keypress)
    root.bind('<KeyRelease>', Control_frame().keyrelease)

    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)


    setup_interface = Setup_frame()
    input_frame = setup_interface.create_setup_frame(root)
    input_frame.grid(column=0, row=0)

    control_interface = Control_frame()
    button_frame = control_interface.create_control_frame(root)
    button_frame.grid(column=1, row=0)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()