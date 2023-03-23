#!/bin/bash


############ Start EV3 RPyC server
echo "Starting EV3 RPyC server"
echo "IP: $1"
gnome-terminal -- bash -c "sshpass -pmaker ssh -t robot@$1 'python3 /home/robot/.local/bin/rpyc_classic.py --host=$1; bash '; exec bash"




