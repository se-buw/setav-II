#!/usr/bin/python3

import rpyc
from curtsies import Input
from ev3_control import Car 


def start_steering(car):
    with Input(keynames='curses') as input_generator:
        while True:
            for e in input_generator:
                print(e)
                if e == 'KEY_LEFT': 
                    car.turn("left")       
                elif e == 'KEY_RIGHT': 
                    car.turn("right")
                elif e == 'KEY_UP': 
                    car.move(500)                           # forward
                    print("forward")
                elif e == 'KEY_DOWN': 
                    car.move(-500)                          # backward
                    print("backward")
                elif e == ' ':                          # stop
                    car.stop()
                elif e == 'p':                          # get angle of the wheels
                    print(car.get_angle()) 
                elif e == '\n':                         # set curent angle of the wheels as zero
                    car.set_zero()
                    print("position zeroed", car.get_angle())

if __name__ == '__main__':
    car = Car()
    start_steering(car)


