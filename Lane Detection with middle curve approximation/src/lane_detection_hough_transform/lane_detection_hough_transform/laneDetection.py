#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rclpy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int64MultiArray
from cv_bridge import CvBridge
from scipy import stats

class lane:
    def __init__ (self,top_l,bottom_l,top_r,bottom_r):
        self.top_l=top_l
        self.bottom_l=bottom_l
        self.top_r=top_r
        self.bottom_r=bottom_r

# converting RGB image to Gray Scale Image

    def grayscale(self,image):  
        return cv.cvtColor(image,cv.COLOR_BGR2GRAY)    

# Getting the prespective of the lane from the top 
    def perspective(self,image): 
      
        pts1=np.float32([self.top_l,self.bottom_l,self.top_r,self.bottom_r])
        pts2=np.float32([[0,0],[0,600],[800,0],[800,600]])
        matrix=cv.getPerspectiveTransform(pts1,pts2)
        return cv.warpPerspective(image,matrix,(800,600))

# Gaussian Blur  to remove noise from the 
    def gaussianFilter(self,image): 
        return cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)

# canny edge detector to determine the edges in the images
    def canny(self,image):
        return cv.Canny(image,5,170)

# Making hough lines as per the edges detected
    def houghlines(self,image):
        return cv.HoughLinesP(image,cv.HOUGH_PROBABILISTIC,theta=np.pi/180,threshold=75,minLineLength=6,maxLineGap=60)

# drawing the lines as per the edges

    def center_line_approximation(self,lines,image):

        right_lane_min_y=10000
        right_lane_max_y=0
        left_lane_points=[[],[]]
        right_lane_points=[[],[]]
        if lines is not None:
            for line in lines:
                    x1,y1,x2,y2 = line[0]
                
                    slope=(y2-y1)/(x2-x1)
                
                    if slope>0:
                        right_lane_points[0].append(x1)
                        right_lane_points[0].append(x2)
                        right_lane_points[1].append(y1)
                        right_lane_points[1].append(y2)
                    
                        
                    else:
                    
                        left_lane_points[0].append(x1)
                        left_lane_points[0].append(x2)
                        left_lane_points[1].append(y1)
                        left_lane_points[1].append(y2)
                        
                
        try:
            res1=np.polyfit(right_lane_points[1],right_lane_points[0],2)
            res2=np.polyfit(left_lane_points[1],left_lane_points[0],2)
        
            right_lane_max_y=max(right_lane_points[1])
            right_lane_min_y=min(right_lane_points[1])
        
        
        
            y_values=np.linspace(right_lane_min_y,right_lane_max_y,10,dtype=int)
            right_x=(res1[0]*y_values**2+res1[1]*y_values+res1[2]).astype(int)
            left_x=(res2[0]*y_values**2+res2[1]*y_values+res2[2]).astype(int)
        
            for i in range(0,9):
                    x1=right_x[i].item()    #converting numpy.int64 to python int
                    y1=y_values[i].item()
                    x2=right_x[i+1].item()
                    y2=y_values[i+1].item()
        
                    cv.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            
            
                    x1=left_x[i].item()    
                    y1=y_values[i].item()
                    x2=left_x[i+1].item()
                    y2=y_values[i+1].item()
        
                    cv.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        
        
        
        
            x_values_center=((res1[0]*y_values**2+res1[1]*y_values+res1[2])+(res2[0]*y_values**2+res2[1]*y_values+res2[2]))//2
            x_values_center=x_values_center.astype(int)			
        
            for i in range(0,9):
                    x1=x_values_center[i].item()    #converting numpy.int64 to python int
                    y1=y_values[i].item()
                    x2=x_values_center[i+1].item()
                    y2=y_values[i+1].item()
        
                    cv.line(image,(x1,y1),(x2,y2),(0,255,0),2)
            
            points=x_values_center.tolist()+y_values.tolist()
            center_lane_points=Int64MultiArray(data=points)
            publisher.publish(center_lane_points)
            print("Lane Detected !")
        
        except:
            pass
            
        return image
    	
    	
    	
    	
        
def convertImage(msg):
        
    image=CvBridge().compressed_imgmsg_to_cv2(msg)
    detect_lane(image)
       
     

def detect_lane(img):
    detect=lane([156.5,71.76],[13.738,114.55],[371.743,64.215],[546.655,126.504])
    img=img[240:480,10:640]
    
    img=detect.perspective(img)
    image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    
    #image=lane.convertImage(msg)
   
    rest,image=cv.threshold(image,190,255,cv.THRESH_BINARY)
    cv.imwrite('binary.jpg',image)
    smooth=detect.gaussianFilter(image)
    smooth=cv.Canny(smooth,5,170)
    cv.imwrite('edge.jpg',smooth)
    
    #cv.imwrite('binary_output.jpg',image)	
    hough=detect.houghlines(image)
    laneDetection=detect.center_line_approximation(hough,img)
    cv.imwrite('detected_lane.jpg',laneDetection)
   
  

    
    
# Compressed Images are subscribed from the raspberry pi 
def main(args=None):

    
    rclpy.init(args=args)
    subscriber_node=rclpy.create_node("Compressed_image_subscriber")
    publisher_node=rclpy.create_node("Lane_publisher")
    
    subscription=subscriber_node.create_subscription(CompressedImage,'/image_raw/compressed',convertImage,10)
    global publisher
    publisher=publisher_node.create_publisher(Int64MultiArray,"lane_coordinates",10)
    
    rclpy.spin(subscriber_node)
    rclpy.spin(publisher_node)
    subscriber_node.destroy_node()
    publisher_node.destroy_node()
    rclpy.shutdown()
    
    
      
    


if __name__=='__main__':
    main()
    
    
"""   lane([173,29],[27,103],[389,29],[585,141])"""
