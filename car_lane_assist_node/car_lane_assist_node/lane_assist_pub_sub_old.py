#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
import random
import numpy as np
import math



class Vehicle(object):

    #intialial position of vehicle
    def __init__(self, x=0.0, y=0.0, angle= 0.0, length=50.0):
        self.difference_distance = 0.0
        self.difference_rotation = 0.0
        self.difference_drift = 0.0
        self.length = length
        self.steer = 0



        #setting coordinates of vehicle
    def set(self, x, y, angle):

        self.x = x
        self.y = y
        self.angle = angle % (2.0 * np.pi)

    def set_difference(self, difference_rotation, difference_distance):
        self.difference_distance = difference_distance
        self.difference_rotation = difference_rotation

    def set_difference_drift(self, drift):
        self.difference_drift = drift

    #steering = angle of front wheel

    def drive(self, steer, distance, tolerance=0.001, max_allowed_steering =np.pi / 4.0):
         if steer > max_allowed_steering:
            steer = max_allowed_steering
         if steer < -max_allowed_steering:
            steer = -max_allowed_steering
         if distance < 0.0:
            distance = 0.0

         steer = random.gauss(steer, self.difference_rotation)
         distance = random.gauss(distance, self.difference_distance)

         steer += self.difference_drift
         

         rotate = np.tan(steer * distance / self.length)
         if abs(rotate) < tolerance:
            
            self.x += distance * np.cos(self.angle)
            self.y += distance * np.sin(self.angle)
            self.angle = (self.angle + rotate) % (2.0 * np.pi)
         else: 
            radius = distance / rotate
            cx = self.x - (np.sin(self.angle) * radius)
            cy = self.y + (np.cos(self.angle) * radius)
            self.angle = (self.angle + rotate) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.angle) * radius)
            self.y = cy - (np.cos(self.angle) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.angle)


class Middle_curve(object):
    def __init__(self):
        self.origin_x = 0
        self.origin_y = 0
        self.x_scaling_factor = 0.00125
        self.y_scaling_factor = 0.00125
        self.total_image_height = 600
        

    def set(self, pixel_x, pixel_y):

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

    def convert_pixels_to_cartesian(self):
        self.x_mid = (self.pixel_x - self.origin_x) * self.x_scaling_factor
        self.y_mid = (self.total_image_height - self.pixel_y - self.origin_y) * self.y_scaling_factor
        #print("Cartesian Coordinate:", self.x_mid, self.y_mid)
        return self.x_mid, self.y_mid
        

    def update_xymid(self, pixel_x, pixel_y):
        self.x_mid, self.y_mid = self.convert_pixels_to_cartesian(pixel_x, pixel_y)



# Publisher node creation class
class lane_assist_publisher(Node):

    def __init__(self):
        super().__init__('lane_assist_pub')
        self.publisher_ = self.create_publisher(String, 'ev3_control_topic', 10)
        # timer_period =  0.01  
        self.publish_msg()
        # self.timer = self.create_timer(timer_period, self.publish_msg)

    def publish_msg(self):
        self.msg = String()
        self.msg.data = command
        self.publisher_.publish(self.msg)
        print(command)

        



# Listner node creation class
class lane_assist_subscriber(Node):

    def __init__(self):
        super().__init__('lane_assist_sub')
        self.subscription = self.create_subscription(Int16MultiArray,"lane_coordinates",self.listener_callback,10)
        self.lane_assist_pub = lane_assist_publisher()

    def listener_callback(self, msg):
        self.get_logger().info('I also heard: "%s"' % msg.data)
    
        middle_curve = Middle_curve()
        x = msg.data[0]
        y = msg.data[1]

        self.middle_curve.set(x,y)
        #middle_curve.set()
        self.middle_curve.x_mid, self.middle_curve.y_mid = self.middle_curve.convert_pixels_to_cartesian()

        self.vehicle = Vehicle()
        self.vehicle.set(0, 0.375, 0)
        self.vehicle.set_difference_drift(10/180.*np.pi)  # add drift bias

        # calculate steer to reach x_mid, y_mid
        self.steer = self.calculate_steer()
        self.steer_angle = self.calculate_steer_angle()
        # drive the vehicle with the calculated steer and a constant speed
        self.vehicle.drive(self.steer, 1)

        print("Pixel location:", self.middle_curve.pixel_x, self.middle_curve.pixel_y)
        print("x_mid & y_mid:", self.middle_curve.x_mid, self.middle_curve.y_mid)
        print("steer angle in degrees", self.steer_angle)
        global command 
        command = "move 30"
        self.lane_assist_pub.publish(command)
        command = "turn %s" %self.steer_angle
        self.lane_assist_pub.publish(command)


# class Emulation_class():
#     def __init__(self):
#         self.middle_curve = Middle_curve()

    # def receive_topic(self):
        

        

    def calculate_steer(self):
        # calculate the desired orientation angle from current position to target
        desired_orientation = np.arctan2(self.middle_curve.y_mid - self.vehicle.y, self.middle_curve.x_mid - self.vehicle.x)
        self.steer = desired_orientation - self.vehicle.angle
        # keep the steer angle between -pi and pi
        self.steer = (self.steer + np.pi/2) % (2 * np.pi/2) - np.pi/2
        print(self.steer)
        return self.steer


    def calculate_steer_angle(self):
        steer_angle = self.steer * 180/math.pi
        #print("angle", steer_angle)
        return steer_angle


def main(args=None):
    
    global command
    command = "set_zero"
    rclpy.init(args = args)
    # lane_assist_pub = lane_assist_publisher()
    lane_assist_sub = lane_assist_subscriber()

    # emulation = Emulation_class()
    rclpy.spin(lane_assist_sub)


    # while(True):
        # emulation.receive_topic()
        # rclpy.spin_once(lane_assist_sub)
        # rclpy.spin_once(lane_assist_pub)
        
    

    lane_assist_pub.destroy_node()
    lane_assist_sub.destroy_node()
    rclpy.shutdown()
    

if __name__=='__main__':
    main()
    
