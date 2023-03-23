**LANE DETECTION USING HOUGH TRANSFORM**

This ROS2 package can be used to detect the lanes using hough transformation method.

Steps to run the package:

1)Source the package using . install/setup.bash command

2)Run the package using ros2 run lane_detection_sliding_window lane_detector command

This package will detect the lanes in the input image and will determine the center of the lanes. Once the center is found ,the pixel coordinates of those points are
published to the "lane_coordinates" topic as a Int64MultiArray message.
