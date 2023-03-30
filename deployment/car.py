#!/usr/bin/python3

import rpyc

# real car class with EV3
class Car():
    def __init__(self,ip) -> None:
        # Setup connections:
        self.conn = rpyc.classic.connect(ip)  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
        ev3 = self.conn.modules['ev3dev.ev3']

        # Set motors outputs:
        self.motor_A = ev3.LargeMotor('outA')    
        self.motor_B = ev3.LargeMotor('outB')
        self.motor_C = ev3.MediumMotor('outC')
        #self.motor_D = ev3.LargeMotor('outD')

        # Set default parameters:
        
        self.wheel_turn_speed = 200

        self.wheel_angle_limit_degrees = 45      # degrees
        self.wheel_step_angle_degrees = 5   # degrees

        self.wheel_angle_coefficient = 80/45        # K coefficient of implses to degrees  deg=imp/K   imp=deg*K
        self.wheel_angle_limit = self.wheel_angle_limit_degrees * self.wheel_angle_coefficient
        self.wheel_step_angle = self.wheel_step_angle_degrees * self.wheel_angle_coefficient

        print("initiated car")
        # self.start_steering(self)

    def destroy(self):
        try:
            self.conn.root.stop()
        except:
            print("Server was closed")


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
        print('position before:'+ str(self.get_angle()))
        if direction == "turn_left":
            if self.get_angle() < self.wheel_angle_limit_degrees:
                self.motor_C.run_to_rel_pos(position_sp = self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn left") 
            else: 
                print("left limit")
                #self.motor_C.position = self.wheel_angle_limit
        elif direction == "turn_right":
            if self.get_angle() > -self.wheel_angle_limit_degrees:
                self.motor_C.run_to_rel_pos(position_sp = -self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn right")
            else: 
                print("right limit")
                #self.motor_C.position = -self.wheel_angle_limit
        print('position after:' + str(self.get_angle())+'\n')
    

    # turn to the given angle to the right (+) or left (-)
    def turn_to_angle(self,angle_deg):
        result_angle = float(angle_deg)*self.wheel_angle_coefficient
        #result_angle = float(self.motor_C.position) - float(angle)
        
        # check if result angle is not exceed max and min limits:
        if result_angle < self.wheel_angle_limit and result_angle > - self.wheel_angle_limit:
            self.motor_C.run_to_abs_pos(position_sp = int(float(result_angle)), speed_sp = self.wheel_turn_speed)
        elif result_angle > self.wheel_angle_limit:
            print("right angle limit reached")
            #self.motor_C.run_to_abs_pos(position_sp = self.wheel_angle_limit, speed_sp = self.wheel_turn_speed)
        elif result_angle < - self.wheel_angle_limit:
            print("left angle limit reached")
            #self.motor_C.run_to_abs_pos(position_sp = -self.wheel_angle_limit, speed_sp = self.wheel_turn_speed)
        print(self.get_angle())


    # stop motor for steering
    def stop_steering(self):
        print("stop steering motor")
        self.motor_C.stop()

    # receive wheels angle position
    def get_angle(self):
        return self.motor_C.position/self.wheel_angle_coefficient

    # set current angle of wheels as reference zero
    def set_zero(self):
        print("set zero:"+str(self.get_angle()))
        self.motor_C.position = 0

    # set default parameters of the car
    def set_parameters(self, step_angle_deg, turn_speed_deg, angle_limit_deg):
        self.wheel_step_angle = step_angle_deg * self.wheel_angle_coefficient
        self.wheel_turn_speed = turn_speed_deg
        self.wheel_angle_limit = angle_limit_deg * self.wheel_angle_coefficient