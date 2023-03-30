#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rclpy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge


class lane:
    def __init__ (self,top_l,bottom_l,top_r,bottom_r):
        self.top_l=top_l
        self.bottom_l=bottom_l
        self.top_r=top_r
        self.bottom_r=bottom_r 

    def perspective(self,image): 
        pts1=np.float32([self.top_l,self.bottom_l,self.top_r,self.bottom_r])
        pts2=np.float32([[0,0],[0,600],[800,0],[800,600]])
        matrix=cv.getPerspectiveTransform(pts1,pts2)
        return cv.warpPerspective(image,matrix,(800,600))


# Compressed Images are subscribed from the raspberry pi 
def detect_lane(img):
    
    print("line detected")
    img=img[160:480,:640]
    detect=lane([189.720,39.405],[22.896,303.403],[387.862    ,40.044],[ 559.159 ,298.290])
    img=detect.perspective(img)
    cv.imwrite("image.jpg",img)
    image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    """cv.imshow("OUtput",image)
    cv.waitKey(5000)"""
    
    #image=lane.convertImage(msg)
   
    rest,image=cv.threshold(image,190,255,cv.THRESH_BINARY)
    cv.imwrite('binary.jpg',image)
    image=cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)
    # try:
    #     leftx,lefty,rightx,righty=detect.search_window(image)   
    #     detect.drawLines(leftx,lefty,rightx,righty,img)
    # except:
    #     print("No lane detected !")

def convertImage(msg):
        
		image=CvBridge().compressed_imgmsg_to_cv2(msg)
		mtx=np.array([[310.05107829,0.,293.37649276],[  0.,309.51905673,254.25816031],[0.,0.,1.]])
		dist=np.array([[-4.67303364e-01,2.26729559e-01,-3.79303222e-04,1.20996005e-04,-5.25339796e-02]])
		image= cv.undistort(image, mtx, dist, None, None)
    
		detect_lane(image)

def main(args=None):
	rclpy.init(args=args)
	subscriber_node=rclpy.create_node("Compressed_image_subscriber")
	publisher_node=rclpy.create_node("Lane_publisher")
    
	subscriber_node.create_subscription(CompressedImage,'/image_raw/compressed',convertImage,10)
    
	rclpy.spin(subscriber_node)
	subscriber_node.destroy_node()
	rclpy.shutdown()


if __name__=='__main__':
    main()