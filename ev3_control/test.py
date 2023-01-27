#!/usr/bin/python3
import os
string = os.popen('ifconfig  | grep 192.168').read()
ip = string.split(' ')
print(ip[9])
