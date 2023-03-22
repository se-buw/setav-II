import torch
from utils.plots import plot_one_box
from utils.general import scale_coords
import cv2

import random

def visualize(im0s,pred,img,names,colors):


	for i, det in enumerate(pred):  
		im0 = im0s[i].copy()
		gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain 
		if len(det):
                
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Bounding box on images
			

			for *xyxy, conf, cls in reversed(det):

				if True: 		 # Add bbox to image
					label = f'{names[int(cls)]} {conf:.2f}'
					c1,c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
					cv2.rectangle(im0, c1, c2, (255,0,0), 1)
					
					
					cv2.putText(im0,label,(c1[0],c1[1]-2),0,1,(255,255,0),1,cv2.LINE_AA)

	
		
		
		return im0,c1,c2
			

