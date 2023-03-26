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
		
		
		projection_matrix=np.array([[-8.30957415e+03 , 0.00000000e+00 , 5.08386041e+02 , 3.50696674e+04],
 [ 0.00000000e+00 ,-8.44691438e+03 , 3.82024835e+02 , 2.16519617e+04],
 [ 0.00000000e+00,  0.00000000e+00 , 6.26181567e-01 , 8.90042603e+01]])/89.0042603
		
			
		objpoints=np.array([p[1],p[0],p[2],1])
		ranges.append(p)
		output=np.dot(projection_matrix,objpoints)
		output=output/output[2]
		if (p[1]>0):
			output[0]=output[0]-320
		image_points.append(output)
	
	return image_points,ranges

    
