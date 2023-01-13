from setuptools import setup

package_name = 'car_control_publisher'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lao',
    maintainer_email='11keitaro@gmail.com',
    description='Keyboard control publisher using rclpy',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = car_control_publisher.keyboard_control_pub:main',
            'listener = car_control_publisher.keyboard_control_sub:main',
        ],
    },
)
