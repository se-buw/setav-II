#!/bin/bash
raspbery_ip="192.168.1.103"
ev3_ip="192.168.1.102"


############ Start EV3 RPyC server
echo "Starting EV3 RPyC server"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t robot@${ev3_ip} 'python3 /home/robot/.local/bin/rpyc_classic.py --host=${ev3_ip}; bash '; exec bash"


############Start raspberry camera publisher Node
echo "Starting raspberry camera publisher Node"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t raspi@${raspbery_ip} 'cd ~/ros2_ws; . install/setup.bash; ros2 run usb_cam usb_cam_node_exe --ros-args --params-file /opt/ros/humble/share/usb_cam/config/params.yaml;  bash'; exec bash"

:''
for i in $(seq 1 35);
do
    echo "sleep: $i"
    sleep 1
done


############Start raspberry listner Node
echo "Start raspberry listner Node"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t raspi@${raspbery_ip} 'cd ~/ros2_ws; . install/setup.bash; ros2 run car_control_publisher listener --ros-args -p ip:='${ev3_ip}';  bash'; exec bash"


############ Start script for control from laptop keyboard (through EV3 - directly) 
echo "Start script for control from laptop keyboard (through EV3 - directly)"
gnome-terminal -- bash -c "cd ~/ros2_ws/src/ev3_control/ ; python3 direct_control_pynput_mult.py ${ev3_ip}; exec bash"
# OR!!!
############ Start script for control from laptop keyboard (through raspberry node - indirectly) 
#echo "Start script for control from laptop keyboard (through raspberry node - indirectly) "
#gnome-terminal -- bash -c "cd ~/ros2_ws/ ; . install/setup.bash; ros2 run car_control_publisher talker;exec bash"



############ Start script for lane assist publisher from raspberry
#echo "Start script for lane assist publisher from raspberry"
#gnome-terminal -- bash -c "sshpass -pmaker ssh -t raspi@${raspbery_ip} 'cd ~/ros2_ws; . install/setup.bash; ros2 run car_lane_assist_node talker;  bash'; exec bash"
# OR!!!
############ Start script for lane assist publisher from laptop
echo "Start script for lane assist publisher from laptop"
gnome-terminal -- bash -c "cd ~/ros2_ws/; . install/setup.bash; ros2 run car_lane_assist_node talker; exec bash"


############ Start script for lane detection using sliding window approach
echo "Start script for lane detection using sliding window approach"
gnome-terminal -- bash -c "cd ~/ros2_ws/src/; python3 'lane detection using sliding window approach.py'; exec bash"
# OR!!!
############ Start script for lane detection using sliding window approach
echo "Start script for Lane Detection with middle curve approximation"
gnome-terminal -- bash -c "cd ~/ros2_ws/src/; python3 'lane detection v5.py'; exec bash"







# Additional sctripts

#gnome-terminal -- bash -c "sshpass -pmaker ssh -t robot@${ev3_ip} 'ls ;echo maker | sudo -S systemctl status rpyc_server_start.service; bash '; exec bash"






