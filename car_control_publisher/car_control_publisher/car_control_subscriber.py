#!/usr/bin/python3

import rpyc
import rclpy
from rclpy.node import Node
from ev3dev.ev3 import *
from std_msgs.msg import String


class Keyboard_control_sub(Node):

    def __init__(self):
        super().__init__('keyboard_control_subscriber')

        self.car=Car()

        self.subscription = self.create_subscription(String,'topic',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        self.message = msg.data.split(" ")
        command = self.message[0]
        if command == "stop": 
            self.car.stop()
        elif command == "move":
            parameter = self.message[1]
            self.car.move(parameter)
        elif command == "left" or command == "right":
            self.car.turn(command)
        elif command == "set_zero":
            self.car.set_zero()
        elif command == "stop_turn" or command == "stop_control":
            print(command)


class emulated_Car():
    def __init__(self) -> None:
        print("initiated emulated   car")

    def turn(self, direction): 
        if direction == "left":
            print("turn left") 
        elif direction == "right":
            print("turn right")

    def move(self,speed):
        print("move")

    def stop(self):
        print("stop")

    def get_angle(self):
        return 20

    def set_zero(self):
        print("set zero")


class Car():
    def __init__(self) -> None:
        # SETUP CONNECTIONS:
        conn = rpyc.classic.connect('192.168.0.121')  # use default TCP port (18812) WIFI:jor: 192.168.0.106 USB:10.42.0.232
        ev3 = conn.modules['ev3dev.ev3']

        # SET MOTORS:
        self.motor_A = ev3.LargeMotor('outA')    # 
        self.motor_B = ev3.LargeMotor('outB')
        self.motor_C = ev3.MediumMotor('outC')
        self.motor_D = ev3.LargeMotor('outD')

        # SET DEFAULT PARAMETERS:
        self.wheel_step_angle = 10
        self.wheel_turn_speed = 700
        self.wheel_angle_limit = 80

        print("initiated car")
        # self.start_steering(self)

    def turn(self,direction):
        if direction == "left":
            if self.motor_C.position < self.wheel_angle_limit:
                self.motor_C.run_to_rel_pos(position_sp = self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn left") 
            else: 
                print("left limit")
                self.motor_C.position = self.wheel_angle_limit
        elif direction == "right":
            if self.motor_C.position > -self.wheel_angle_limit:
                self.motor_C.run_to_rel_pos(position_sp = -self.wheel_step_angle, speed_sp = self.wheel_turn_speed)
                print("turn right")
            else: 
                print("right limit")
                self.motor_C.position = -self.wheel_angle_limit
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

    def set_parameters(self, step_angle, turn_speed, angle_limit):
        self.wheel_step_angle = step_angle
        self.wheel_turn_speed = turn_speed
        self.wheel_angle_limit = angle_limit
        pass


def main(args=None):

    rclpy.init(args=args)

    keyboard_control_subscriber = Keyboard_control_sub()

    rclpy.spin(keyboard_control_subscriber)

    keyboard_control_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()