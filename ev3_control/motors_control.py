#!/usr/bin/python3

import rpyc
from ev3dev.ev3 import *
from curtsies import Input

conn = rpyc.classic.connect('192.168.0.106')  # use default TCP port (18812)
ev3 = conn.modules['ev3dev.ev3']
motor_A = ev3.LargeMotor('outA')    # 
motor_B = ev3.LargeMotor('outB')
motor_C = ev3.MediumMotor('outC')
motor_D = ev3.LargeMotor('outD')

def main():
    start_steering()
def start_steering():
    with Input(keynames='curses') as input_generator:
        motor_C.position=0
        while True:
            for e in input_generator:
                print(repr(e))
                if e == 'KEY_LEFT': 
                    turn("left")   
                    print("turn left")     
                elif e == 'KEY_RIGHT': 
                    turn("right")
                    print("turn right")
                elif e == 'KEY_UP': 
                    move(400)                           # forward
                    print("forward")
                elif e == 'KEY_DOWN': 
                    move(-400)                          # backward
                    print("backward")
                elif e == ' ':                          # get angle of the wheels
                    print(motor_C.position) 
                elif e == '\n':                         # set curent angle of the wheels as zero
                    motor_C.position=0
                    print("position zeroed", motor_C.position) 


def turn(direction):
    if direction == "left":
        if motor_C.position<80:
            motor_C.run_to_rel_pos(position_sp=15,speed_sp=50)
        else: 
            print("left limit")
            motor_C.position = 110
    elif direction == "right":
        if motor_C.position>-80:
            motor_C.run_to_rel_pos(position_sp=-15,speed_sp=50)
        else: 
            print("right limit")
            motor_C.position = -110
    print(motor_C.position)

def move(speed):
    motor_A.run_forever(speed_sp=int(speed))
    motor_B.run_forever(speed_sp=-int(speed))   

# def forward(time=300, speed=400):
#     motor_A.run_timed(time_sp = time, speed_sp = speed)
#     motor_B.run_timed(time_sp = time, speed_sp = -speed)
#     print("forward")

# def backward(time=300, speed=400):
#     print(motor_C.position)
#     motor_A.run_timed(time_sp = time, speed_sp = -speed)
#     motor_B.run_timed(time_sp = time, speed_sp =  speed)
#     print("backward")


if __name__ == '__main__':
    main()


