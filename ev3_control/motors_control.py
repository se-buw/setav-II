#!/usr/bin/python3

import rpyc
from ev3dev.ev3 import *
from curtsies import Input

conn = rpyc.classic.connect('192.168.0.110')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
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
                print(e)
                if e == 'KEY_LEFT': 
                    turn("left")       
                elif e == 'KEY_RIGHT': 
                    turn("right")
                elif e == 'KEY_UP': 
                    move(500)                           # forward
                    print("forward")
                elif e == 'KEY_DOWN': 
                    move(-500)                          # backward
                    print("backward")
                elif e == ' ':                          # stop
                    stop()
                elif e == 'p':                          # get angle of the wheels
                    print(motor_C.position) 
                elif e == '\n':                         # set curent angle of the wheels as zero
                    motor_C.position=0
                    print("position zeroed", motor_C.position)


def turn(direction):
    if direction == "left":
        if motor_C.position<80:
            motor_C.run_to_rel_pos(position_sp = 25,speed_sp=350)
            print("turn left") 
        else: 
            print("left limit")
            motor_C.position = 80
    elif direction == "right":
        if motor_C.position>-80:
            motor_C.run_to_rel_pos(position_sp = -25,speed_sp=350)
            print("turn right")
        else: 
            print("right limit")
            motor_C.position = -80
    print(motor_C.position)

def move(speed):
    motor_A.run_forever(speed_sp=int(speed))
    motor_B.run_forever(speed_sp=-int(speed))

def stop():
    print("stop")
    motor_A.stop()
    motor_B.stop()

if __name__ == '__main__':
    main()


