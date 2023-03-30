#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int64MultiArray
import random
import numpy as np
import math



class Middle_curve():
    def __init__(self):

        self.x_scaling_factor = 0.001
        self.y_scaling_factor = 0.000625
        self.total_image_height = 600
        

    def set(self, pixel_x1, pixel_y1, pixel_x2, pixel_y2):
        self.origin_x = pixel_x1
        self.origin_y = pixel_y1
        self.pixel_x = pixel_x2
        self.pixel_y = pixel_y2

    def convert_pixels_to_cartesian(self):
        self.x_mid = (self.pixel_x - self.origin_x) * self.x_scaling_factor
        self.y_mid = (self.total_image_height - self.pixel_y - self.origin_y) * self.y_scaling_factor
        #print("Cartesian Coordinate:", self.x_mid, self.y_mid)
        return self.x_mid, self.y_mid
        



# Publisher node creation class
class Lane_assist_publisher(Node):

    def __init__(self):
        super().__init__('lane_assist_pub')
        print("lane assist publisher_ initialized")
        self.publisher_ = self.create_publisher(String, 'ev3_control_topic', 10)
        # timer_period =  0.01  
        #self.publish_msg("")
        # self.timer = self.create_timer(timer_period, self.publish_msg)

    def publish_msg(self,command):
        self.msg = String()
        self.msg.data = command
        self.publisher_.publish(self.msg)
        print(command)

        

# Listner node creation class
class Lane_assist_subscriber(Node):

    def __init__(self):
        super().__init__('lane_assist_sub')
        print("lane assist subscriber initialized")
        self.subscription = self.create_subscription(Int64MultiArray,"lane_coordinates",self.listener_callback,10)
        self.subscription
        self.lane_assist_pub = Lane_assist_publisher()

    def listener_callback(self, msg):
        #self.get_logger().info('callback received')
        #self.get_logger().info('I also heard: "%s"' % msg.data)
    
        self.middle_curve = Middle_curve()

        # nearest middle line point
        x1 = msg.data[0]    # X - horisontal    point (0,0) is in left upper corner of the lane 
        y1 = msg.data[600]  # Y - vertical

        # 
        x1 = 400
        y1 = 600
        # 100th middle line point
        x2 = msg.data[99]
        y2 = msg.data[700]

        print("x1 , y1", x1, y1)
        print("x2 , y2", x2, y2)
        
        self.middle_curve.set(x1,y1,x2,y2)
        self.middle_curve.x_mid, self.middle_curve.y_mid = self.middle_curve.convert_pixels_to_cartesian()

        self.steer_angle = self.calculate_steer_angle()

        global command 
        global speed
        speed = 50
        command = "move 50"
        # self.lane_assist_pub.publish_msg(command)
        self.steer_angle = self.steer_angle


        # print("Pixel location:", self.middle_curve.pixel_x, self.middle_curve.pixel_y)
        #print("x_mid & y_mid:", self.middle_curve.x_mid, self.middle_curve.y_mid)
        print("angle to steer in degrees", self.steer_angle)
        command = "turn_to_angle %s" %self.steer_angle
        self.lane_assist_pub.publish_msg(command)



    def calculate_steer_angle(self):
        self.steer = np.arctan2(self.middle_curve.y_mid, self.middle_curve.x_mid)
        
        steer_angle = self.steer * 180/math.pi
        self.steer = (self.steer + np.pi/2) % (2 * np.pi/2) - np.pi/2
        
        #print("angle", steer_angle)
        return steer_angle


def main(args=None):
    
    global command
    command = "set_zero"
    rclpy.init(args = args)
    lane_assist_sub = Lane_assist_subscriber()
    rclpy.spin(lane_assist_sub)



    # lane_assist_pub.destroy_node()
    lane_assist_sub.destroy_node()
    rclpy.shutdown()
    

if __name__=='__main__':
    main()
    
