#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rclpy
from sensor_msgs.msg import CompressedImage
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



    def drawLines(self,image,img):
    
    	image1=image[:,0:(image.shape[1]//2)]
    	image2=np.array(image[:,(image.shape[1]//2)+1:])
    	zero=np.zeros((image.shape[0],(image.shape[1]//2)))
    	image2=np.concatenate((zero,image2),axis=1)
    	
    
    	nonzero1=np.nonzero(image1)
    	nonzero2=np.nonzero(image2)
    	left_points_x=nonzero1[1]
    	left_points_y=nonzero1[0]
    	right_points_x=nonzero2[1]
    	right_points_y=nonzero2[0]
                			
                		
    	
    	res1=np.polyfit(right_points_y,right_points_x,2)
    	res2=np.polyfit(left_points_y,left_points_x,2)
    	
    	right_lane_max_y=600
    	right_lane_min_y=0
    	
    	
    	
    	y_values=np.linspace(right_lane_min_y,right_lane_max_y,10,dtype=int)
    	right_x=(res1[0]*y_values**2+res1[1]*y_values+res1[2]).astype(int)
    	left_x=(res2[0]*y_values**2+res2[1]*y_values+res2[2]).astype(int)
    	
    	
    	
    	for i in range(0,9):
    		x1=right_x[i].item()    #converting numpy.int64 to python int
    		y1=y_values[i].item()
    		x2=right_x[i+1].item()
    		y2=y_values[i+1].item()
    	
    		cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    		
    		
    		x1=left_x[i].item()    
    		y1=y_values[i].item()
    		x2=left_x[i+1].item()
    		y2=y_values[i+1].item()
    	
    		cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    	
    	
    	x_values_center=((res1[0]*y_values**2+res1[1]*y_values+res1[2])+(res2[0]*y_values**2+res2[1]*y_values+res2[2]))//2
    	x_values_center=x_values_center.astype(int)
    	
    	
    	
    	for i in range(0,9):
    		x1=x_values_center[i].item()    #converting numpy.int64 to python int
    		y1=y_values[i].item()
    		x2=x_values_center[i+1].item()
    		y2=y_values[i+1].item()
    	
    		cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    	
    		
    	
    	  
    	return img
        
        
        
        
    def convertImage(msg):
        
        image=CvBridge().compressed_imgmsg_to_cv2(msg)
	#image=CvBridge().imgmsg_to_cv2(msg)
	#result.write(image)
	#cv.imwrite("trainingImages/lane_image_"+str(count)+".jpg",image)
	#count+=1
        return image
       
     

    
    
# Compressed Images are subscribed from the raspberry pi 
def main():
    
    img=cv.imread('lane_image_0.jpg',cv.IMREAD_COLOR)
    img=img[240:480,10:640]
    detect=lane([173,29],[27,103],[389,29],[585,141])
    img=detect.perspective(img)
    image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    
    
    #image=lane.convertImage(msg)
   
    rest,image=cv.threshold(image,190,255,cv.THRESH_BINARY)
    cv.imwrite('binary.jpg',image)
    smooth=detect.gaussianFilter(image)
    laneDetection=detect.drawLines(smooth,img)
    cv.imshow("Detected Lane and Center",laneDetection)
    cv.waitKey(5000)
    cv.imwrite('detected_lane.jpg',laneDetection)
    cv.destroyAllWindows
    
    


if __name__=='__main__':
    main()
    
    
  