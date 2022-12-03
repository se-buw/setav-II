#!/usr/bin/python3

import rpyc
from ev3dev.ev3 import *
import keyboard

################################# initialisation of control
conn = rpyc.classic.connect('192.168.0.110')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
ev3 = conn.modules['ev3dev.ev3']
motor_A = ev3.LargeMotor('outA')    
motor_B = ev3.LargeMotor('outB')
motor_C = ev3.MediumMotor('outC')
motor_D = ev3.LargeMotor('outD') 

def main():
    start_steering()

################################# input listening
def start_steering():
    while True:
        event = keyboard.read_event()                                           # Wait for the next event.
        #print(event.name)
        if event.event_type == keyboard.KEY_DOWN and event.name == 'up':        # start forward
            print('up pressed')
            move(500)
        elif event.event_type == keyboard.KEY_UP and event.name == 'up':        # stop 
            stop()
            print('up released')
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'down':    # start backward
            move(-500)
            print('down pressed')
        elif event.event_type == keyboard.KEY_UP and event.name == 'down':      # stop 
            stop()
            print('down released')  
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'left':    # left
            turn("left")
            print('left pressed')
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'right':   # right
            turn("right")
            print('right pressed')
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'p':       # wheel angle
            print(motor_C.position)
            print('p pressed')
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'enter':   # zero wheel angle
            motor_C.position=0
            print('enter pressed')
        elif event.event_type == keyboard.KEY_DOWN and event.name == 'space':   # stop
            print('space pressed')

################################# turn left or right
def turn(direction):                            
    if direction == "left":
        if motor_C.position<90:
            motor_C.run_to_rel_pos(position_sp = 25,speed_sp=350)
            print("turn left") 
        else: 
            print("left limit")
            motor_C.position = 90
    elif direction == "right":
        if motor_C.position>-90:
            motor_C.run_to_rel_pos(position_sp = -25,speed_sp=350)
            print("turn right")
        else: 
            print("right limit")
            motor_C.position = -90
    print(motor_C.position)


################################# move forvard non-stop

def move(speed):                                
    motor_A.run_forever(speed_sp=int(speed))
    motor_B.run_forever(speed_sp=-int(speed))

################################# stop
def stop():                                     
    print("stop")
    motor_A.stop()
    motor_B.stop()

if __name__ == '__main__':
    main()