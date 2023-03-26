#!/bin/bash


############ Start script for lane assist publisher from laptop
echo "Start script for lane assist publisher from laptop"
gnome-terminal -- bash -c "cd ~/ros2_ws/; . install/setup.bash; ros2 run car_lane_assist_node talker; exec bash"
