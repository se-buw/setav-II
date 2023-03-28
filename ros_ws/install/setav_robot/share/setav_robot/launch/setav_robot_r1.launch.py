import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

  #Setting  the path to different files and folders.
  
  
  pkg_share = FindPackageShare(package='setav_robot').find('setav_robot')
  launch_dir = os.path.join(pkg_share, 'launch')
  model_path = os.path.join(pkg_share, 'models/setav_robot_r1.urdf')
  robot_name_in_urdf = 'setav_robot'
  rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
  
  # Launch config variables
  
  gui = LaunchConfiguration('gui')                                  #variable used to  specify whether to launch the GUI for the simulation.
  model = LaunchConfiguration('model')                              #variable is used to specify the path to the URDF file for the robot model.
  rviz_config_file = LaunchConfiguration('rviz_config_file')        #variable is used to specify the path to the RViz configuration file for the simulation.
  use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')  #variable is used to specify whether to use the robot_state_publisher node.
  use_rviz = LaunchConfiguration('use_rviz')                        #variable is used to specify whether to launch RViz.
  use_sim_time = LaunchConfiguration('use_sim_time')                #variable is used to specify whether to use simulated time instead of wall-clock time.

  # Declare the launch arguments  
  declare_model_path = DeclareLaunchArgument(
    name='model', 
    default_value=model_path)
    
  declare_rviz_config_file = DeclareLaunchArgument(
    name='rviz_config_file',
    default_value=rviz_config_path)
    
  declare_use_joint_state_publisher = DeclareLaunchArgument(
    name='gui',
    default_value='True')
  
  declare_use_robot_state_pub = DeclareLaunchArgument(
    name='use_robot_state_pub',
    default_value='True')

  declare_use_rviz = DeclareLaunchArgument(
    name='use_rviz',
    default_value='True')
    
  declare_use_sim_time = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True')
   
  # Specify the actions

  # Publish the joint state values for the non-fixed joints in the URDF file.
  start_joint_state_publisher = Node(
    condition=UnlessCondition(gui),
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher')

  # A GUI to manipulate the joint state values
  start_joint_state_publisher_gui = Node(
    condition=IfCondition(gui),
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui',
    name='joint_state_publisher_gui')

  # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
  start_robot_state_publisher = Node(
    condition=IfCondition(use_robot_state_pub),
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'use_sim_time': use_sim_time, 
    
    'robot_description': Command(['xacro ', model])}],
    arguments=[model_path])

  # Launch RViz
  start_rviz = Node(
    condition=IfCondition(use_rviz),
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
    arguments=['-d', rviz_config_file])
  
  # Create the launch description 
  launch_des = LaunchDescription()

  # Declare the launch options
  launch_des.add_action(declare_model_path)
  launch_des.add_action(declare_rviz_config_file)
  launch_des.add_action(declare_use_joint_state_publisher)
  launch_des.add_action(declare_use_robot_state_pub)  
  launch_des.add_action(declare_use_rviz) 
  launch_des.add_action(declare_use_sim_time)

  
  launch_des.add_action(start_joint_state_publisher)
  launch_des.add_action(start_joint_state_publisher_gui)
  launch_des.add_action(start_robot_state_publisher)
  launch_des.add_action(start_rviz)

  return launch_des
