#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray


# Publisher node creation class
class lane_assist_publisher(Node):

    def __init__(self):
        super().__init__('lane_assist_pub')
        self.publisher_ = self.create_publisher(String, 'ev3_control_topic', 10)
        timer_period =  0.01  
        self.timer = self.create_timer(timer_period, self.publish_msg)

    def publish_msg(self):
        self.msg = String()
        self.msg.data = "stop"
        self.publisher_.publish(self.msg)



# Listner node creation class
class lane_assist_subscriber(Node):

    def __init__(self):
        super().__init__('lane_assist_sub')
        self.subscription = self.create_subscription(String,'topic',self.listener_callback,10)

    def listener_callback(self, msg):
        self.get_logger().info('I also heard: "%s"' % msg.data)


def main(args=None):
    
    rclpy.init(args = args)
    lane_assist_pub = lane_assist_publisher()
    lane_assist_sub = lane_assist_subscriber()
    while(True):
        rclpy.spin_once(lane_assist_pub)
        rclpy.spin_once(lane_assist_sub)
        
    

    lane_assist_pub.destroy_node()
    lane_assist_sub.destroy_node()
    rclpy.shutdown()
    

if __name__=='__main__':
    main()
    