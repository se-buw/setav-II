import rclpy
from rclpy.node import Node
import cv2 as cv
from sensor_msgs.msg import CompressedImage, LaserScan,Image
from message_filters import Subscriber, ApproximateTimeSynchronizer
import lidar
from objectDetection import ObjectDetection
import math
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        
        self.subscriber1 = Subscriber(self,CompressedImage, '/image_raw/compressed')
        self.subscriber2 = Subscriber(self, LaserScan, '/scan_filtered')
        self.approx_sync = ApproximateTimeSynchronizer([self.subscriber1, self.subscriber2], 10, 30000)
        self.approx_sync.registerCallback(self.callback)

    def callback(self, img_msg, lidar_msg):
        # do something with the messages
        
        image_points,ranges=lidar.test(lidar_msg)
        
        output_image,c1,c2=ObjectDetection.callback(img_msg)
        lidar_points=[]
        final_ranges=[]
        x1=c1[0]
        y1=c1[1]
        x2=c2[0]
        y2=c2[1]
        for j,i in enumerate(image_points):
        	if ((i[0]>=x1 and i[0]<=x2) and (i[1]>=y1 and i[1]<=y2)):
        		lidar_points.append((int(i[0]),int(i[1])))
        		x=ranges[j][0]
        		y=ranges[j][1]
        		distance=math.sqrt((x**2+y**2))
        		final_ranges.append(distance)
        		
        	else:
        		lidar_points.append((int(i[0]),int(i[1])))  
        		x=ranges[j][0] # have to remoove this finally as we need to draw lidar points only inside the box
        		y=ranges[j][1]
        		distance=math.sqrt((x**2+y**2))
        		final_ranges.append(distance)
        
        for i in lidar_points:
        	cv.circle(output_image,i,2,(0,0,255),2)
        
        distance_of_object=round(sum(final_ranges)/len(final_ranges),2)
        
        cv.putText(output_image,str(distance_of_object)+"m",(c1[0]-3,c1[1]-4),0,1,(255,255,0),1,cv.LINE_AA)
        cv.imshow("OUtput",output_image)
        cv.waitKey(1000)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

