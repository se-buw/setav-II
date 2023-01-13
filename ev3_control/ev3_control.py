#!/usr/bin/python3

import rpyc
from ev3dev.ev3 import *
from curtsies import Input

# class Car():
#     def __init__(self) -> None:
#         print("initiated car")

#     def turn(self, direction): 
#         if direction == "left":
#             print("turn left") 
#         elif direction == "right":
#             print("turn right")

#     def move(self,speed):
#         print("move")

#     def stop(self):
#         print("stop")

#     def get_angle(self):
#         return 20

#     def set_zero(self):
#         print("set zero")

class Car():
    def __init__(self) -> None:
        conn = rpyc.classic.connect('192.168.0.121')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
        ev3 = conn.modules['ev3dev.ev3']
        self.motor_A = ev3.LargeMotor('outA')    # 
        self.motor_B = ev3.LargeMotor('outB')
        self.motor_C = ev3.MediumMotor('outC')
        self.motor_D = ev3.LargeMotor('outD')
        print("initiated car")
        # self.start_steering(self)

    def turn(self,direction):
        if direction == "left":
            if self.motor_C.position<80:
                self.motor_C.run_to_rel_pos(position_sp = 15,speed_sp=450)
                print("turn left") 
            else: 
                print("left limit")
                self.motor_C.position = 80
        elif direction == "right":
            if self.motor_C.position>-80:
                self.motor_C.run_to_rel_pos(position_sp = -15,speed_sp=450)
                print("turn right")
            else: 
                print("right limit")
                self.motor_C.position = -80
        print(self.motor_C.position)

    def move(self,speed):
        print("move")
        self.motor_A.run_forever(speed_sp=int(speed))
        self.motor_B.run_forever(speed_sp=-int(speed))

    def stop(self):
        print("stop")
        self.motor_A.stop()
        self.motor_B.stop()

    def get_angle(self):
        return self.motor_C.position

    def set_zero(self):
        print("set zero")
        self.motor_C.position = 0

if __name__ == '__main__':
    c=Car()
    c.main(c)


