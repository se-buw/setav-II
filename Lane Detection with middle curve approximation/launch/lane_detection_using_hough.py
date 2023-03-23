from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
    
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            parameters=['params.yaml'],
           
        ),
        Node(
            package='lane_detection_hough_transform',
            executable='lane_detector',
            
        ),
          Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            
        ),  
        Node(
            package='laser_filters',
            executable='scan_to_scan_filter_chain',
            parameters=['angleRange_filter.yaml'],
            
        ),
        ]
        )
   
