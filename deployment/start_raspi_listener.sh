#!/bin/bash

############Start raspberry listner Node
echo "Start raspberry listner Node"
echo "raspbery ip: $1"
echo "ev3_ip: $2"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t raspi@$1 'cd ~/ros2_ws; . install/setup.bash; ros2 run car_control_publisher listener --ros-args -p ip_ev3:=$2;  bash'; exec bash"




