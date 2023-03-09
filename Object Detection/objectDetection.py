import numpy as np
import cv2 as cv
import torch
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, apply_classifier
from utils.torch_utils import load_classifier
import visualize
from multiprocessing import Process
import rclpy
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import PointCloud2,LaserScan
import laser_geometry.laser_geometry as lg
import math
import os


class ObjectDetection:


	model = attempt_load("yolov7.pt", map_location="cpu")  # load FP32 model
	stride = int(model.stride.max())  # model stride
	imgsz = check_img_size(640, s=stride)  # check img_size
	names = model.module.names if hasattr(model, 'module') else model.names
	colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]	

	
	

	def callback(msg):
		
		image=CvBridge().compressed_imgmsg_to_cv2(msg)
		
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
	

