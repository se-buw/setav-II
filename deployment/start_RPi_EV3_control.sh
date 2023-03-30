#!/bin/bash



echo "Start laptop->raspberry->ev3 publisher Node"
#echo "raspbery ip: $1"
gnome-terminal -- bash -c "cd ~/ros2_ws; . install/setup.bash; ros2 run car_control_publisher talker "
