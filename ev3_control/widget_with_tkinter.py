#!/usr/bin/python3
import tkinter as tk
import os
os.system('xset r off')

def return_pressed(event):
    print('Return key pressed.')


def keypress(event):
    print("keypress")
    if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
        print("keypress")
    else:
        return

def keyrelease(event):
    print("KeyRelease")

root = tk.Tk()
root.bind('<KeyPress>', keypress)
root.bind('<KeyRelease>', keyrelease)
root.mainloop()