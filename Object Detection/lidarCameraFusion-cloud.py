import rclpy
from rclpy.node import Node
import cv2 as cv
from sensor_msgs.msg import CompressedImage, LaserScan,Image
from message_filters import Subscriber, ApproximateTimeSynchronizer
import lidar
from objectDetection import ObjectDetection
import math
from std_msgs.msg import String
import numpy as np
class Fusion(Node):
    def __init__(self):
        super().__init__('my_node')
        
        self.subscriber1 = Subscriber(self,CompressedImage, '/image_raw/compressed')
        self.subscriber2 = Subscriber(self, LaserScan, '/scan_filtered')
        publisher_node=rclpy.create_node("Detected_objects_publisher")
        global publisher
        publisher=publisher_node.create_publisher(String,"detected_objects",10)
        
        self.approx_sync = ApproximateTimeSynchronizer([self.subscriber1, self.subscriber2], 10,20000)
        self.approx_sync.registerCallback(self.callback)

    def callback(self, img_msg, lidar_msg):
        # do something with the messages
        
        image_points,ranges=lidar.test(lidar_msg)
       
        
        output_image,detected_object_points=ObjectDetection.callback(img_msg)
        final_output=[]
        
        for k in range(len(detected_object_points)):
        	lidar_points=[]
        	final_ranges=[]
        	c1=detected_object_points[k][0]
        	c2=detected_object_points[k][1]
       
        	x1=c1[0]
        	y1=c1[1]
        	x2=c2[0]
        	y2=c2[1]
        	for j,i in enumerate(image_points):
        		if ((i[0]>=x1 and i[0]<=x2) and (i[1]>=y1 and i[1]<=y2)):
        			lidar_points.append((int(i[0]),int(i[1])))
        		
        			final_ranges.append(ranges[j])
        		
        		else:
        			lidar_points.append((int(i[0]),int(i[1])))
        			
        	if(len(final_ranges)!=0):
        		final_output.append([c1,c2,final_ranges])
        	for i in lidar_points:
        		cv.circle(output_image,i,2,(0,0,255),2)
        
        	       			
       			
       	
       	msg=String()
       	msg.data=str(final_output)
       	
       	publisher.publish(msg)     				
        cv.imshow("OUtput",output_image)
        cv.waitKey(4000)

def main(args=None):
    rclpy.init(args=args)
    node = Fusion()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

