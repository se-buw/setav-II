#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rclpy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from scipy import stats
import matplotlib.pyplot as plt
from std_msgs.msg import Int64MultiArray

from matplotlib import pyplot as plt

class lane:
    def __init__ (self,top_l,bottom_l,top_r,bottom_r):
        self.top_l=top_l
        self.bottom_l=bottom_l
        self.top_r=top_r
        self.bottom_r=bottom_r 

# Getting the prespective of the lane from the top 
    def perspective(self,image): 
        
        pts1=np.float32([self.top_l,self.bottom_l,self.top_r,self.bottom_r])
        pts2=np.float32([[0,0],[0,600],[800,0],[800,600]])
        matrix=cv.getPerspectiveTransform(pts1,pts2)
        return cv.warpPerspective(image,matrix,(800,600))

# Gaussian Blur  to remove noise from the 
    def gaussianFilter(self,image): 
        return cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)


    def drawLines(self,leftx,lefty,rightx,righty,image):
        	
    	
        y_values=np.linspace(image.shape[0]-1,0,image.shape[0],dtype=int)
        try:
            res1=np.polyfit(lefty,leftx,2)
            res2=np.polyfit(righty,rightx,2)
            print(res1)
            print(res2)
            left_x=(res1[0]*y_values**2+res1[1]*y_values+res1[2]).astype(int)
            right_x=(res2[0]*y_values**2+res2[1]*y_values+res2[2]).astype(int)
            center_x=(left_x+right_x)//2
            plt.imshow(image)
            plt.plot(left_x,y_values,color="red")
            plt.plot(right_x,y_values,color="red")
            plt.plot(center_x,y_values,color="green")
            plt.show()
            points=center_x.tolist()+y_values.tolist()
            center_lane_points=Int64MultiArray(data=points)
            publisher.publish(center_lane_points)
            print("Lane Detected !")

        except:
            pass
            print("exception")

	
       
    def search_window(self,image):
        histogram=np.sum(image,axis=0)
        midpoint=np.int64(histogram.shape[0]//2)
        left_current_x=np.argmax(histogram[:midpoint])
        right_current_x=np.argmax(histogram[midpoint:])+midpoint
        
        if (right_current_x-left_current_x)>300:
            number_of_windows=9
            margin=100
            minPixels=50
            window_height=np.int64(image.shape[0]//number_of_windows)
        
            nonzero_y=np.nonzero(image)[0]
            nonzero_x=np.nonzero(image)[1]
    	
    	
            left_lane_indexes=[]
            right_lane_indexes=[]
    	
            for window in range(number_of_windows):
                window_y_low=image.shape[0]-(window+1)*window_height
                window_y_high=image.shape[0]-window*window_height
    	
                win_xleft_low = left_current_x - margin
                win_xleft_high = left_current_x + margin
                win_xright_low = right_current_x - margin
                win_xright_high = right_current_x + margin    
    		 		
    		
                good_left_inds = ((nonzero_y >= window_y_low) & (nonzero_y < window_y_high) & 
                (nonzero_x >= win_xleft_low) &  (nonzero_x < win_xleft_high)).nonzero()[0]
                good_right_inds = ((nonzero_y >= window_y_low) & (nonzero_y < window_y_high) & 
                (nonzero_x >= win_xright_low) &  (nonzero_x < win_xright_high)).nonzero()[0]	
    		
    		
                left_lane_indexes.append(good_left_inds)
                right_lane_indexes.append(good_right_inds)
    	
                if len(good_left_inds)>50:
                    left_current_x=np.int64(np.mean(nonzero_x[good_left_inds]))
                if len(good_right_inds)>50:
                    right_current_x=np.int64(np.mean(nonzero_x[good_right_inds]))
    			
    	
            left_lane_indexes=np.concatenate(left_lane_indexes)
            right_lane_indexes=np.concatenate(right_lane_indexes)
    
            leftx = nonzero_x[left_lane_indexes]
            lefty = nonzero_y[left_lane_indexes] 
            rightx = nonzero_x[right_lane_indexes]
            righty = nonzero_y[right_lane_indexes]
    	
    	
            return leftx,lefty,rightx,righty
    		

    
    
# Compressed Images are subscribed from the raspberry pi 
def detect_lane(img):
    
    print("est")
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
    image=detect.gaussianFilter(image)
    try:
        leftx,lefty,rightx,righty=detect.search_window(image)   
        detect.drawLines(leftx,lefty,rightx,righty,img)
    except:
        print("No lane detected !")
    
    
    
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
    
    
  



""" lane([159.04,   3.06],
       [  4.95,  61.98],
       [401.25,   4.85],
       [573.23,  67.93])  perspective transform points"""
