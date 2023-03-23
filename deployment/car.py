#!/usr/bin/python3

import rpyc

# real car class with EV3
class Car():
    def __init__(self) -> None:
        # Setup connections:
        conn = rpyc.classic.connect('192.168.1.108')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
        ev3 = conn.modules['ev3dev.ev3']

        # Set motors outputs:
        self.motor_A = ev3.LargeMotor('outA')    
        self.motor_B = ev3.LargeMotor('outB')
        self.motor_C = ev3.MediumMotor('outC')
        #self.motor_D = ev3.LargeMotor('outD')

        # Set default parameters:
        self.wheel_step_angle = 10
        self.wheel_turn_speed = 700
        self.wheel_angle_limit = 80
        self.wheel_angle_coefficient = 5        # comand value devided to real degrees 

        print("initiated car")
        # self.start_steering(self)


    # infinite move with chosen speed forward (+) or backward (-)
    def move(self,speed):
        print("move")
        self.motor_A.run_forever(speed_sp=int(speed))
        self.motor_B.run_forever(speed_sp=-int(speed))

    # stop of main motors
    def stop_main_motors(self):
        print("stop main motors")
        self.motor_A.stop()
        self.motor_B.stop()

    # turn to the right or left to one step (step_angle parameter)
    def turn_left_or_right(self,direction):
        if direction == "turn_left":
            if self.motor_C.position < self.wheel_angle_limit:
                self.motor_C.run_to_rel_pos(position_sp = self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn left") 
            else: 
                print("left limit")
                self.motor_C.position = self.wheel_angle_limit
        elif direction == "turn_right":
            if self.motor_C.position > -self.wheel_angle_limit:
                self.motor_C.run_to_rel_pos(position_sp = -self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn right")
            else: 
                print("right limit")
                self.motor_C.position = -self.wheel_angle_limit
        print(self.motor_C.position)
    
    # turn to the given angle to the right (+) or left (-)
    def turn_to_angle(self,angle):
        angle = angle*self.wheel_angle_coefficient
        result_angle = self.motor_C.position + float(angle)
        # check if result angle is not exceed max and min limits:
        if result_angle < self.wheel_angle_limit and result_angle > - self.wheel_angle_limit:
            self.motor_C.run_to_abs_pos(position_sp = int(float(angle)), speed_sp = self.wheel_turn_speed)
        elif result_angle > self.wheel_angle_limit:
            print("right angle limit reached")
            self.motor_C.run_to_abs_pos(position_sp = self.wheel_angle_limit, speed_sp = self.wheel_turn_speed)
            # self.motor_C.position = self.wheel_angle_limit
        elif result_angle < - self.wheel_angle_limit:
            print("left angle limit reached")
            self.motor_C.run_to_abs_pos(position_sp = -self.wheel_angle_limit, speed_sp = self.wheel_turn_speed)
            # self.motor_C.position = - self.wheel_angle_limit
        print(self.motor_C.position)

    # stop motor for steering
    def stop_steering(self):
        print("stop steering motor")
        self.motor_C.stop()

    # receive wheels angle position - NOT IMPLEMENTED 
    def get_angle(self):
        return self.motor_C.position

    # set current angle of wheels as reference zero
    def set_zero(self):
        print("set zero")
        self.motor_C.position = 0

    # set default parameters of the car
    def set_parameters(self, step_angle, turn_speed, angle_limit):
        self.wheel_step_angle = step_angle
        self.wheel_turn_speed = turn_speed
        self.wheel_angle_limit = angle_limit