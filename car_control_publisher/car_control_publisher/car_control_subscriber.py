#!/usr/bin/python3

import rpyc
import rclpy
from .car import Car
from .emulated_Car import Emulated_Car
from rclpy.node import Node
from ev3dev.ev3 import *
from std_msgs.msg import String

# Priority management:
# default priority of control (priority_level =2)
#       ros2 run car_control_publisher listener
# Manual control through ROS2 priority_level =1:
#       ros2 run car_control_publisher listener --ros-args -p priority_level:=1
# Direct control of EV3 priority_level =0:
#       ros2 run car_control_publisher listener --ros-args -p priority_level:=0

# Start real usage:
#       ros2 run car_control_publisher listener
# To start emulated car:
#       ros2 run car_control_publisher listener --ros-args -p emulation:=True
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
# check_zero
# set_zero
# set_parameters step_angle turn_speed angle_limit
# stop_turn


# Node creation class
class Keyboard_control_sub(Node):

    def __init__(self):
        super().__init__('keyboard_control_subscriber')


        # Choose car type, default: emulation = False
        self.declare_parameter('emulation', False)
        emulation = self.get_parameter('emulation').get_parameter_value().bool_value
        if emulation == True:
            self.car=Emulated_Car()
        else:
            # Choose pripority_level, default: pripority_level = 2
            self.declare_parameter('pripority_level', 2)
            self.pripority_level = self.get_parameter('pripority_level').get_parameter_value().integer_value
            if self.pripority_level == 2:
                print ("switch to default automatic control (priority level=2)")
                self.car=Car()
            elif self.pripority_level == 1:
                print ("switch to remote control (priority level=1)")
                self.car=Car()
            elif self.pripority_level == 0:
                print ("switch to direct control (priority level=0)")

        

        self.subscription = self.create_subscription(String,'ev3_control_topic',self.listener_callback,10)
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
        elif command == "check_zero":
            self.car.turn_to_angle(0)
        elif command == "set_zero":
            self.car.set_zero()
        elif command == "set_parameters":
            step_angle = self.message[1]
            turn_speed = self.message[2]
            angle_limit = self.message[3]
            self.set_parameters(step_angle, turn_speed, angle_limit)
        elif command == "stop_turn":
            self.car.stop_steering()




def main(args=None):

    rclpy.init(args=args)

    keyboard_control_subscriber = Keyboard_control_sub()

    rclpy.spin(keyboard_control_subscriber)

    keyboard_control_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()