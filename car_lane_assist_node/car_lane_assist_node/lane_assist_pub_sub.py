#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray


class Vehicle(object):

    #intialial position of vehicle
    def __init__(self, x=0.0, y=0.0, angle= 0.0, length=50.0):
        self.difference_distance = 0.0
        self.difference_rotation = 0.0
        self.difference_drift = 0.0
        self.length = length

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

    
    def run(self, wp, wd, wi, n=100, speed=2.0):
        x_trajectory = []
        y_trajectory = []
        
        prev_cte = self.y
        sum_cte = 0
        for _ in range(n):
            sum_cte += self.y
            dev = self.y - prev_cte
            prev_cte = self.y
            steer = -wp * self.y - wd * dev - wi*sum_cte
            self.drive(steer, speed)
            x_trajectory.append(self.x)
            y_trajectory.append(self.y)
            print(steer)
        
        # write a code to derive angles from the steer
        angles = []
        return angles

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.angle)



# Publisher node creation class
class lane_assist_publisher(Node):

    def __init__(self):
        super().__init__('lane_assist_pub')
        self.publisher_ = self.create_publisher(String, 'ev3_control_topic', 10)
        timer_period =  0.01  
        self.timer = self.create_timer(timer_period, self.publish_msg)

    def publish_msg(self):
        self.msg = String()
        self.msg.data = command
        self.publisher_.publish(self.msg)



# Listner node creation class
class lane_assist_subscriber(Node):

    def __init__(self):
        super().__init__('lane_assist_sub')
        self.subscription = self.create_subscription(Int16MultiArray,"lane_coordinates",self.listener_callback,10)

    def listener_callback(self, msg):
        self.get_logger().info('I also heard: "%s"' % msg.data)
    
        vehicle = Vehicle()
        x = msg.data[0]
        y = msg.data[1]
        vehicle.set(x,y)
        angles = vehicle.run()
        global command
        for angle in angles:
            command= "turn_to_angle %s" %angle



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
    