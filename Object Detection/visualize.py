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
					
					plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

	
		
		number=random.randint(0,1000)
		cv2.imwrite("./output/output"+str(number)+".jpg", im0)
			

