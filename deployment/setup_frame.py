#!/usr/bin/python3
import tkinter as tk
from tkinter import TclError, ttk
import subprocess

class Setup_frame():
    def __init__(self) -> None:
        self.emulation = True
        print("initiated car")


    def start_ev3serv(ip_ev3):
        print('ip_ev3 ',ip_ev3.get())
        Setup_frame.save_to_file("ip_ev3.txt",ip_ev3.get())
        subprocess.run(["./start_ev3serv.sh", ip_ev3.get()])

    def start_raspi_listener_node(ip_rasp,ip_ev3):
        Setup_frame.save_to_file("ip_ev3.txt",ip_ev3.get())
        Setup_frame.save_to_file("ip_rasp.txt",ip_rasp.get())
        print('ip_rasp ',ip_rasp.get())
        subprocess.run(["./start_raspi_listener.sh", ip_rasp.get(), ip_ev3.get()])

    def start_camera_lidar(ip_rasp):
        print('ip_rasp ',ip_rasp.get())
        Setup_frame.save_to_file("ip_rasp.txt",ip_rasp.get())
        subprocess.run(["./start_camera_lidar.sh", ip_rasp.get()])

    def start_RPi_EV3_control():
        subprocess.run(["./start_RPi_EV3_control.sh"])
    
    def start_lane_assistance_publisher(ip_rasp):
        subprocess.run(["./start_lane_assistance_publisher.sh", ip_rasp.get()])


    def save_to_file(file,var):
        file = open(file, "w")
        file.write(var)
        file.close()


    def create_setup_frame(self,container):

        frame = ttk.Frame(container)

        # grid layout for the input frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        # Input ev3 Brick IP
        ev3_IP = tk.StringVar()
        ttk.Label(frame, text='EV3 IP:').grid(column=0, row=0, sticky=tk.W)
        ev3_IP_entry = ttk.Entry(frame, width=30,textvariable=ev3_IP)
        ev3_IP_entry.insert(1,string='192.168.1.103')
        ev3_IP_entry.grid(column=1, row=0, sticky=tk.W)
        ev3_button = ttk.Button(frame, text='Start EV3 RpyC server', command=lambda: Setup_frame.start_ev3serv(ev3_IP))
        ev3_button.grid(column=2, row=0)

        # Raspberry IP listner enable
        raspi_IP = tk.StringVar()
        ttk.Label(frame, text='Raspberry IP:').grid(column=0, row=1, sticky=tk.W)
        rasp_IP_entry = ttk.Entry(frame, width=30,textvariable=raspi_IP)
        rasp_IP_entry.insert(1,string='192.168.1.100')
        rasp_IP_entry.grid(column=1, row=1, sticky=tk.W)
        raspi_button = ttk.Button(frame, text='Start raspberry listner', command=lambda: Setup_frame.start_raspi_listener_node(raspi_IP,ev3_IP))
        raspi_button.grid(column=2, row=1)

        # Raspberry camera and lidar enable script
        raspi_button = ttk.Button(frame, text='Enable camera and lidar', command=lambda: Setup_frame.start_camera_lidar(raspi_IP))
        raspi_button.grid(column=0, row=2)
        ttk.Label(frame, text='Status:').grid(column=1, row=2, sticky=tk.W)

        # Raspberry camera and lidar fusion enable script
        raspi_button = ttk.Button(frame, text='Camera and lidar fusion', command=lambda: Setup_frame.start_raspi_listener_node(raspi_IP,ev3_IP))
        raspi_button.grid(column=0, row=3)

        # Raspberry Lane detection publisher script
        raspi_button = ttk.Button(frame, text='RPi -> ev3 control', command=lambda: Setup_frame.start_RPi_EV3_control()).grid(column=2, row=4)

        # Lane following
        ttk.Button(frame, text='Lane follow start', command=lambda: Setup_frame.start_lane_assistance_publisher(raspi_IP)).grid(column=0, row=5)
        #ttk.Button(frame, text='Lane follow stop', command=lambda: Setup_interface.start_lane_detection_publisher()).grid(column=1, row=5) 
        # ttk.Label(frame, text='Status:').grid(column=2, row=5, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)
        return frame