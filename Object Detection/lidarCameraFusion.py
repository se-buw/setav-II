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
        super().__init__('LidarCameraFusion node')
        
        self.subscriber1 = Subscriber(self,CompressedImage, '/image_raw/compressed')
        self.subscriber2 = Subscriber(self, LaserScan, '/scan_filtered')
        publisher_node=rclpy.create_node("Detected_objects_publisher")
        global publisher
        publisher=publisher_node.create_publisher(String,"detected_objects",10)
        
        self.approx_sync = ApproximateTimeSynchronizer([self.subscriber1, self.subscriber2], 10,2)
        self.approx_sync.registerCallback(self.callback) #callback method is called when the image and lidar data are in sync

    def callback(self, img_msg, lidar_msg):
        
        #Converts lidar messages to point cloud and projects those point cloud over the camera's image plane
        image_points,ranges=lidar.convert_to_point_cloud(lidar_msg)
       
        #Detects the objects present in the input image and returns the position of detected objects in the image
        output_image,detected_object_points=ObjectDetection.callback(img_msg)
        final_output=[]
        #Finds the projected lidar points that are within the bounding boxes of the detected objects
        for k in range(len(detected_object_points)):
        	lidar_points=[]
        	final_ranges=[]
        	updated_ranges=[]
        	c1=detected_object_points[k][0]
        	c2=detected_object_points[k][1]
       
        	x1=c1[0]
        	y1=c1[1]
        	x2=c2[0]
        	y2=c2[1]
        	for j,i in enumerate(image_points):
        		# Draws the projected lidar points inside the bounding boxes when they are found within the range
        		if ((i[0]>=x1 and i[0]<=x2) and (i[1]>=y1 and i[1]<=y2)):
        			lidar_points.append((int(i[0]),int(i[1])))
        			x=ranges[j][0]
        			y=ranges[j][1]
        			updated_ranges.append(ranges[j])
        			distance=math.sqrt((x**2+y**2))
        			final_ranges.append(distance)
        		
        		else:
        			lidar_points.append((int(i[0]),int(i[1])))
        			x=ranges[j][0]
        			y=ranges[j][1]
        			distance=math.sqrt((x**2+y**2))
        			
        
	
        	for i in lidar_points:
        		cv.circle(output_image,i,2,(0,0,255),2)
        
        	if (len(final_ranges)!=0):
        
        		distance_of_object=round(sum(final_ranges)/len(final_ranges),2)
        
       			cv.putText(output_image,str(distance_of_object)+"m",(c2[0]-3,c2[1]-4),0,0.5,(255,255,0),1,cv.LINE_AA)
       			final_output.append([c1,c2,updated_ranges])
       			
       	#Publishes the lidar points(as point cloud) that are present inside the bounding boxes 
       	msg=String()
       	msg.data=str(final_output)
       	
       	publisher.publish(msg)     				
        cv.imshow("OUtput",output_image)
        cv.waitKey(400)

def main(args=None):
    rclpy.init(args=args)
    node = Fusion()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

