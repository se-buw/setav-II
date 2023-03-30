#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
from emulated_Car import Emulated_Car 
from car import Car 

class Control_frame():
    def __init__(self) -> None:
        self.emulation = tk.StringVar()
        #self.emulation.set(0)
        self.car=Emulated_Car()
        self.set_emulation(0)

        self.speed = 100


    def create_control_frame(self,container):
        frame = ttk.Frame(container)
        frame.focus_set()

            # add Key capture
        container.bind('<KeyPress>', self.keypress)
        container.bind('<KeyRelease>', self.keypress)

        frame.columnconfigure(0, weight=1)

        angle = tk.StringVar()
        ttk.Entry(frame, width=4,textvariable=angle).grid(column=1, row=0, sticky=tk.W)
        ttk.Button(frame, text='Turn to angle:', command=lambda: self.car.turn_to_angle(angle.get())).grid(column=0, row=0)
        ttk.Button(frame, text='Set zero', command=lambda: self.car.set_zero()).grid(column=2, row=0)

        ttk.Button(frame, text='Forward', command=lambda: self.car.move(self.speed)).grid(column=1, row=1)
        ttk.Button(frame, text='Left', command=lambda: self.car.turn_left_or_right("turn_left")).grid(column=0, row=2)
        ttk.Button(frame, text='Right', command=lambda: self.car.turn_left_or_right("turn_right")).grid(column=2, row=2)
        ttk.Button(frame, text='Backward', command=lambda: self.car.move(-self.speed)).grid(column=1, row=2)
        ttk.Button(frame, text='Stop', command=lambda: self.car.stop_main_motors()).grid(column=1, row=3)
        ttk.Button(frame, text='Connect to the car', command=lambda: self.set_emulation('0')).grid(column=0, row=4)
        ttk.Button(frame, text='Disconnect (emulate)', command=lambda: self.set_emulation('1')).grid(column=2, row=4)
        
        # Emulation checkbox
        match_case_check = ttk.Checkbutton(frame, text='Use emulated car', variable=self.emulation,
            command=lambda: self.set_emulation(self.emulation.get()))
        match_case_check.grid(column=0, row=5, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame
    
    def keypress(self,event):
        if event.keysym == 'Up':
            self.car.move(self.speed)
        elif event.keysym == 'Down':
           self.car.move(-self.speed)
        elif event.keysym == 'Left':
            self.car.turn_left_or_right("turn_left")
        elif event.keysym == 'Right':
            self.car.turn_left_or_right("turn_right")
        elif event.keysym == 'space':
            self.car.stop_main_motors()
        elif  event.keysym == 'Control_L' or event.keysym == 'Control_R':
            self.car.get_angle()
        elif event.keysym == 'Return':
            self.car.set_zero()
        else:
            return
        

    def keyrelease(self,event):
        if event.keysym == 'Left' or event.keysym == 'Right':
            self.car.stop_steering()
            print("stop_steering")
        


    def set_emulation(self, check_box):
        self.emulation.set(check_box)
        if check_box == '1':
            print('disconnection...')
            self.car.destroy()
            self.car=Emulated_Car()
            print('emulation enabled, disconnected from the real car')
        elif check_box  == '0':
            print('connection...')
            ip_ev3 = open('ip_ev3.txt').read()
            self.car=Car(ip_ev3)
            print('emulation disabled, connected to the real car')
        else: print ("incorrect emulation parameter")
    
    def forward(self):
        print("sada")

    