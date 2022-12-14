import rclpy
from cv_bridge import CvBridge
import cv2 as cv
from sensor_msgs.msg import CompressedImage



count=0


#This script is used collect images from the RPi camera for generating object detection dataset

def callback(msg):
	global count
	image=CvBridge().compressed_imgmsg_to_cv2(msg)
	#image=CvBridge().imgmsg_to_cv2(msg)
	cv.imwrite("trainingImages/lane_image_"+str(count)+".jpg",image)
	count+=1


def main(args=None):
	rclpy.init(args=args)
	node=rclpy.create_node("Compressed_image_subscriber")
	subscription=node.create_subscription(CompressedImage,'/image_raw/compressed',callback,10)
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()





if __name__=="__main__":
	main()


