#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import os
import glob

class lane:

    transformation_matrix_inverse=[]
    def __init__ (self,top_l,bottom_l,top_r,bottom_r):
        self.top_l=top_l
        self.bottom_l=bottom_l
        self.top_r=top_r
        self.bottom_r=bottom_r

# converting RGB image to Gray Scale Image

    def grayscale(self,image):  
        return cv.cvtColor(image,cv.COLOR_BGR2GRAY)    

# Getting the prespective of the lane from the top 
    def persective(self,image): 
        global transformation_matrix_inverse
        pts1=np.float32([self.top_l,self.bottom_l,self.top_r,self.bottom_r])
        pts2=np.float32([[0,0],[0,800],[800,0],[800,800]])
        transformation_matrix=cv.getPerspectiveTransform(pts1,pts2)
        transformation_matrix_inverse=cv.getPerspectiveTransform(pts2,pts1)
        return cv.warpPerspective(image,transformation_matrix,(800,800))

# Gaussian Blur  to remove noise from the 
    def gaussianFilter(self,image): 
        return cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)

# canny edge detector to determine the edges in the images
    def canny(self,image):
        return cv.Canny(image,5,170)

# Making hough lines as per the edges detected
    def houghlines(self,image):
        return cv.HoughLinesP(image,cv.HOUGH_PROBABILISTIC,theta=np.pi/180,threshold=85,minLineLength=30,maxLineGap=300)

# drawing the lines as per the edges

    def drawLines(self,lines,image,filename):
    	right_lane_points=[[],[]]
    	left_lane_points=[[],[]]    	
    	
    	
    	for line in lines:
    		
    		x1,y1,x2,y2 = line[0]
    		slope=0
    		if x2!=x1:
    			slope= (y2-y1)/(x2-x1)
    		#print(slope)
    			if slope>0:
    				right_lane_points[0].append(x1)
    				right_lane_points[0].append(x2)
    				right_lane_points[1].append(y1)
    				right_lane_points[1].append(y2)
	                	
	                	
	                	
    			elif slope<0 :
    			
    				left_lane_points[0].append(x1)
    				left_lane_points[0].append(x2)
    				left_lane_points[1].append(y1)
    				left_lane_points[1].append(y2)
                		
                
               	
    	left_lane_min_x=min(left_lane_points[0])
    	left_lane_max_x=max(left_lane_points[0])
    	left_lane_min_y=min(left_lane_points[1])
    	left_lane_max_y=max(left_lane_points[1])
        
    	right_lane_min_x=min(right_lane_points[0])
    	right_lane_max_x=max(right_lane_points[0])
    	right_lane_min_y=min(right_lane_points[1])
    	right_lane_max_y=max(right_lane_points[1])
    	
    
    	cv.rectangle(image,(left_lane_min_x,left_lane_min_y),(left_lane_max_x,left_lane_max_y),(0,255,0),2)
    	cv.rectangle(image,(right_lane_min_x,right_lane_min_y),(right_lane_max_x,right_lane_max_y),(0,255,0),2)
    	
    	width_of_left_lane=(left_lane_max_x-left_lane_min_x)
    	height_of_left_lane=(left_lane_max_y-left_lane_min_y)
    	width_of_right_lane=(right_lane_max_x-right_lane_min_x)
    	height_of_right_lane=(right_lane_max_y-right_lane_min_y)
    	
    	avg_left_x=sum(left_lane_points[0])//len(left_lane_points[0])
    	avg_left_y=sum(left_lane_points[1])//len(left_lane_points[1])
    	
    	avg_right_x=sum(right_lane_points[0])//len(right_lane_points[0])
    	avg_right_y=sum(right_lane_points[1])//len(right_lane_points[1])
    	
    	
    	output="0 {min_x} {min_y} {width} {height}".format(min_x=avg_left_x,min_y=avg_left_y,width=width_of_left_lane,height=height_of_left_lane) +"\n"+"0 {min_x} {min_y} {width} {height}".format(min_x=avg_right_x,min_y=avg_right_y,width=width_of_right_lane,height=height_of_right_lane)
    	filename=filename.split(".")[0]+".txt"
    	
    	f=open("./labels/{name}".format(name=filename),"w")
    	f.write(output)
    	
    	f.close() 
    	return image
    	
    	
   

    
    
# Compressed Images are subscribed from the raspberry pi 
def main():
    path1="./croppedImages/"
    path2="./annotatedImages/"
    path3="./birdViewAnnotation/"
    
    
    for filename in glob.glob("*.jpg"):
    
	
    	img=cv.imread(filename,cv.IMREAD_COLOR)
    	img=img[240:480,10:640]
    	cv.imwrite(os.path.join(path1,filename),img)

    	detect=lane([173,29],[27,103],[389,29],[585,141])
    	#detect=lane([148,31],[25,100],[404,34],[582,133]) these values are also good
    	bird_view=detect.persective(img)
    	image=cv.cvtColor(bird_view,cv.COLOR_BGR2GRAY)
    	rest,image=cv.threshold(image,190,255,cv.THRESH_BINARY)
    	smooth=detect.gaussianFilter(image)
    	smooth=cv.Canny(smooth,5,170)
    	hough=detect.houghlines(image)
    	laneDetection=detect.drawLines(hough,bird_view,filename)
    	cv.imwrite(os.path.join(path3,filename),laneDetection)
    	image=cv.warpPerspective(laneDetection,transformation_matrix_inverse,(800,800))
    	cv.imwrite(os.path.join(path2,filename),image)



if __name__=='__main__':
    main()
    
    
    
   
