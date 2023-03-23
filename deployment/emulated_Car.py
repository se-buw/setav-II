#!/usr/bin/python3

# emulated car class for testing
class Emulated_Car():
    def __init__(self) -> None:
        print("initiated emulated   car")

    def turn_left_or_right(self, direction): 
        if direction == "left":
            print("turn left") 
        elif direction == "right":
            print("turn right")

    def move(self,speed):
        print("move with speed: %s" %speed)

    def turn_to_angle(self,angle):
        print("turn to angle: %s" %angle)

    def stop_main_motors(self):
        print("stop main motors")

    def stop_steering(self):
        print("stop steering motors")

    def get_angle(self):
        return 20

    def set_zero(self):
        print("set current wheel angle as zero")

        