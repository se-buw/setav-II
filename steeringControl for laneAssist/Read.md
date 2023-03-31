

Here you will find two approaches of Steering Control for lane assist and steering control for obstacle avoidance using A*:

Direct steering angle calculation for lane assist: this file subscribes data from Lane detection which is coordinates of middle curve of lane lines. After processing data and calculating steering angle is then published for further use.

Steering angle calculation by PID control technique for lane assist: you will find implementation of PID approach to calculate steering angle.


Steering Control for obstacle avoidance using A*: This file receives input data from LiDAR which contains co-ordinates of obstacles. 2D grid map is generated and according to received data from LiDAR, cells are marked as occupied where obstacles are present. Size and position of obstacles are considered for planning a path to reach target position. At the end it gives accurate path which avoids obstacles.
