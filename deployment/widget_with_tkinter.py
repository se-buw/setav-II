#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
import os

from  control_interface import Control_interface
from  setup_interface import Setup_interface

os.system('xset r off')

def return_pressed(event):
    print('Return key pressed.')


def keypress(event):
    print("keypress")
    if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
        print("Shift")
    else:
        return

def keyrelease(event):
    print("KeyRelease")



def create_main_window():
    root = tk.Tk()
    root.title('Replace')
    root.resizable(0, 0)

    # add Key capture
    root.bind('<KeyPress>', keypress)
    root.bind('<KeyRelease>', keyrelease)

    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    setup_interface = Setup_interface()
    input_frame = setup_interface.create_setup_frame(root)
    input_frame.grid(column=0, row=0)

    control_interface = Control_interface()
    button_frame = control_interface.create_control_frame(root)
    button_frame.grid(column=1, row=0)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()