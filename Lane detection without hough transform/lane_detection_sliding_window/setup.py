from setuptools import setup

package_name = 'lane_detection_sliding_window'

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
    maintainer='gstark',
    maintainer_email='gouthamanstark@gmail.com',
    description='TODO: Lane detection using sliding window',
    license='TODO: Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['lane_detector = lane_detection_sliding_window.lane:main',
        ],
    },
)
