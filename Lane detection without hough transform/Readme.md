**LANE DETECTION USING SLIDING WINDOW APPROACH**

This ROS2 package can be used to detect the lanes using the sliding window approach.

Steps to run the package:

1)Source the package using . install/setup.bash command from the "Lane Detection without hough transform" folder.

2)Navigate into the launch folder using "cd launch" command.
3)Run the ROS2 launch file with the "ros2 launch lane_detection_using_sliding_window.py" commmand.

Running this launch file will start the usb_cam,rplidar,scan_to_scan filter (angleRange filter) and lane detection nodes.


This will detect the lanes in the input image and will determine the center of the lanes. Once the center is found ,the pixel coordinates of those points are
published to the "lane_coordinates" topic as a Int64MultiArray message.
