#!/bin/bash

############Start raspberry camera publisher Node
echo "Starting raspberry camera publisher Node"
echo "raspbery ip: $1"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t raspi@${1} 'cd ~/ros2_ws; . install/setup.bash; ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /opt/ros/humble/share/usb_cam/config/params.yaml;  bash'; exec bash"


