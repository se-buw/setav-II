#!/usr/bin/env python3

import rclpy
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray


def test_method(test_parameter):
    print("test")


def main(args=None):
    
    rclpy.init(args = args)
    subscriber_node = rclpy.create_node("lane_detection_subscriber")
    publisher_node = rclpy.create_node("car_control_commands_publisher")

    subscription = subscriber_node.create_subscription(Int16MultiArray,"lane_coordinates",test_method,10)
    publisher = publisher_node.create_publisher(String,"control_commands",10)

    rclpy.spin(subscriber_node)
    
    rclpy.spin(publisher_node)

    subscriber_node.destroy_node()
    publisher_node.destroy_node()
    rclpy.shutdown()
    

if __name__=='__main__':
    main()
    