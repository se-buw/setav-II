#!/bin/bash



echo "Start script for Lane Detection with middle curve approximation"
gnome-terminal -- bash -c "cd ~/ros2_ws/src/; python3 'lane detection v5.py'; exec bash"
