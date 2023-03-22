import rclpy
from sensor_msgs.msg import PointCloud2,LaserScan
import laser_geometry.laser_geometry as lg
import math
import point_cloud2
import numpy as np

def test(lidar_msg):
	lp=lg.LaserProjection()
	point_cloud_msg=lp.projectLaser(lidar_msg)
	print("lidar Data!!")
	return save(point_cloud_msg)


def save(msg):
	
	image_points=[]
	ranges=[]
	points = np.ndarray(
        shape=(msg.width * msg.height, ),
        dtype=point_cloud2.dtype_from_fields(msg.fields, point_step=msg.point_step),
        buffer=msg.data)
	
        
	

	gen=point_cloud2.read_points(msg,field_names = ("x", "y", "z"), skip_nans=False)
	for p in gen:
		"""
		projection_matrix=np.array([[ 4.10887273e+02,-2.24133502e+01,1.13449233e+02,17.15941827e+02],
 		[ 1.15310118e+02,2.51585852e+02,2.89581412e+02,1.13198914e+03],
 		[ 4.64931601e-01,-1.96191343e-01,8.63335139e-01,7.11292144e+00]])"""
		projection_matrix=np.array([[ 3.80674031e+02,-1.13763053e+02 , 1.56034251e+02 , 1.66550161e+03],
 [ 7.98412750e+01 , 1.22816512e+02  ,3.72814611e+02 , 1.39583343e+03],
 [ 2.84812786e-01, -5.33151264e-01 , 7.96637563e-01 , 9.04908883e+00]])
		objpoints=np.array([p[0],p[1],p[2],1])
		ranges.append(p)
		output=np.dot(projection_matrix,objpoints)
		output=output/output[2]
		image_points.append(output)
	
	return image_points,ranges

    
