#!/usr/bin/python3

import rpyc
import rclpy
from rclpy.node import Node
from ev3dev.ev3 import *
from std_msgs.msg import String

# Commands to control car:
# std_msgs.msg.String with space separation: "command parameter"
# 
# list of comands:
#
# move speed-parameter
# stop
# turn_to_angle angle
# turn_left
# turn_right
# set_zero
# set_parameters step_angle turn_speed angle_limit
# stop_turn


# Node creation class
class Keyboard_control_sub(Node):

    def __init__(self):
        super().__init__('keyboard_control_subscriber')

        self.car=Emulated_Car()

        self.subscription = self.create_subscription(String,'topic',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.message = msg.data.split(" ")
        command = self.message[0]
        if command == "stop": 
            self.car.stop_main_motors()
        elif command == "move":
            speed = self.message[1]
            self.car.move(speed)
        elif command == "turn_to_angle":
            angle = self.message[1]
            self.car.turn_to_angle(angle)
        elif command == "turn_left" or command == "turn_right":
            self.car.turn_left_or_right(command)
        elif command == "set_zero":
            self.car.set_zero()
        elif command == "set_parameters":
            step_angle = self.message[1]
            turn_speed = self.message[2]
            angle_limit = self.message[3]
            self.set_parameters(step_angle, turn_speed, angle_limit)
        elif command == "stop_turn":
            self.car.stop_steering()


# real car class with EV3
class Car():
    def __init__(self) -> None:
        # Setup connections:
        conn = rpyc.classic.connect('192.168.0.121')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
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
        result_angle = self.motor_C.position + angle
        # check if result angle is not exceed max and min limits:
        if result_angle < self.wheel_angle_limit and result_angle > - self.wheel_angle_limit:
            self.motor_C.run_to_rel_pos(position_sp = result_angle, speed_sp = self.wheel_turn_speed)
        elif result_angle > self.wheel_angle_limit:
            print("right angle limit reached")
            self.motor_C.position = self.wheel_angle_limit
        elif result_angle < - self.wheel_angle_limit:
            print("left angle limit reached")
            self.motor_C.position = - self.wheel_angle_limit
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


def main(args=None):

    rclpy.init(args=args)

    keyboard_control_subscriber = Keyboard_control_sub()

    rclpy.spin(keyboard_control_subscriber)

    keyboard_control_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()