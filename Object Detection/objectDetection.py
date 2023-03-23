import numpy as np
import cv2 as cv
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression
import visualize
from multiprocessing import Process
import rclpy
from cv_bridge import CvBridge



class ObjectDetection:


	model = attempt_load("yolov7.pt", map_location="cpu")  # load FP32 model
	names = model.module.names if hasattr(model, 'module') else model.names
	colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]	

	
	

	def callback(msg):
		
		image=CvBridge().compressed_imgmsg_to_cv2(msg)
		mtx=np.array([[310.05107829,0.,293.37649276],[  0.,309.51905673,254.25816031],[0.,0.,1.]])
		
		dist=np.array([[-4.67303364e-01,2.26729559e-01,-3.79303222e-04,1.20996005e-04,-5.25339796e-02]])
		image= cv.undistort(image, mtx, dist, None, None)
		
		list1=[image]
		img=list1
		#process=Process(target=ObjectDetection.object_detection,args=(img,list1))
		#process.start()
		return ObjectDetection.object_detection(img,list1)
		
	

	def object_detection(img,list1):
	
		
	
		img = np.stack(img, 0)
	
		img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
		img = np.ascontiguousarray(img)
		img = torch.from_numpy(img).to("cpu")
		img = img.float()  # uint8 to fp16/32
		img /= 255.0  # 0 - 255 to 0.0 - 1.0
		if img.ndimension() == 3:
			img = img.unsqueeze(0)
		
		#Inference
		with torch.no_grad():   
			pred = ObjectDetection.model(img, augment=False)[0]
		
		pred = non_max_suppression(pred, 0.5, 0.45, classes=None, agnostic=False)

		

		return visualize.visualize(list1,pred,img,ObjectDetection.names,ObjectDetection.colors)
	

