**LIDAR AND CAMERA SENSOR FUSION FOR ESTIMATING THE DISTANCE OF OBJECTS**

This python script is used to estimate the distance of the objects around the car by fusing the LIDAR and camera data.Time synchronized data from the camera and 
the lidar is used by this script. The LaserScan messages received from the lidar(from /scan_filtered topic) is converted into pointcloud data and the obtained 
pointcloud data is projected into the camera's image plane using the projection matrix of the camera.

YoloV7 algorithm is used to detect and recognize the objects in the input image and bounding boxes are drawn around them.The projected lidar points which
are present inside the bounding boxes are considered to be reflected from the detected objects and the point cloud data of those lidar points are used to determine 
the distance of that respective object.

The position of the detected objects and their respective point cloud data is published as a String message to the "detected_objects" topic.

**STEPS TO RUN THE SCRIPT**
Run the script with "Python3 lidarCameraFusion.py"
(please make sure that you run either Lane detection using hough transform launch file or the sliding_window launch file before running this script.)
