#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
import subprocess

class Setup_interface():
    def __init__(self) -> None:
        self.emulation = True
        print("initiated car")

    def set_emulation(self,check_box):
        print('emulation =',check_box)
        self.emulation = check_box


    def start_ev3serv(ip_ev3):
        print('ip_ev3',ip_ev3.get())
        subprocess.run(["./start_ev3serv.sh", ip_ev3.get()])

    def start_raspi_listener_node(ip_rasp,ip_ev3):
        print('ip_rasp',ip_rasp.get())
        subprocess.run(["./start_raspi_listener.sh", ip_rasp.get(), ip_ev3.get()])


    def create_setup_frame(self,container):

        frame = ttk.Frame(container)

        # grid layout for the input frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        # Input ev3 Brick IP
        ev3_IP = tk.StringVar()
        ttk.Label(frame, text='EV3 IP:').grid(column=0, row=0, sticky=tk.W)
        ev3_IP_entry = ttk.Entry(frame, width=30,textvariable=ev3_IP)
        ev3_IP_entry.insert(1,string='192.168.1.102')
        ev3_IP_entry.grid(column=1, row=0, sticky=tk.W)
        ev3_button = ttk.Button(frame, text='Start EV3 RpyC server', command=lambda: Setup_interface.start_ev3serv(ev3_IP))
        ev3_button.grid(column=2, row=0)

        # Raspberry IP
        raspi_IP = tk.StringVar()
        ttk.Label(frame, text='Raspberry IP:').grid(column=0, row=1, sticky=tk.W)
        rasp_IP_entry = ttk.Entry(frame, width=30,textvariable=raspi_IP)
        rasp_IP_entry.insert(1,string='192.168.1.103')
        rasp_IP_entry.grid(column=1, row=1, sticky=tk.W)
        raspi_button = ttk.Button(frame, text='Enable camera and lidar', command=lambda: Setup_interface.start_raspi_listener_node(raspi_IP,ev3_IP))
        raspi_button.grid(column=2, row=1)

        # Lane following
        ttk.Button(frame, text='Lane follow start').grid(column=0, row=2)
        ttk.Button(frame, text='Lane follow stop').grid(column=1, row=2) 
        ttk.Label(frame, text='Status:').grid(column=2, row=2, sticky=tk.W)

        # Emulation checkbox
        match_case = tk.StringVar()
        match_case_check = ttk.Checkbutton(
            frame,
            text='Use emulated car',
            variable=match_case,
            command=lambda self: self.set_emulation(self,match_case.get()))
        match_case_check.grid(column=0, row=5, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)
        return frame