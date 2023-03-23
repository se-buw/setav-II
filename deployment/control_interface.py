#!/usr/bin/python3
from tkinter import TclError, ttk

class Control_interface():
    def __init__(self) -> None:

        print("initiated car")


    def create_control_frame(self,container):
        frame = ttk.Frame(container)

        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text='Forward', command=lambda: Control_interface.forward()).grid(column=1, row=0)
        ttk.Button(frame, text='Left', command=lambda: Control_interface.left()).grid(column=0, row=1)
        ttk.Button(frame, text='Right', command=lambda: Control_interface.right()).grid(column=2, row=1)
        ttk.Button(frame, text='Backward', command=lambda: Control_interface.backward()).grid(column=1, row=1)
        ttk.Button(frame, text='STOP', command=lambda: Control_interface.stop()).grid(column=1, row=2)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame
    
    def forward():
        print("sada")