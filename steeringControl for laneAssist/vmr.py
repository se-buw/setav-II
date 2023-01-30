
import random
import numpy as np
import math


class Vehicle(object):

    #intialial position of vehicle
    def __init__(self, x=0.0, y=0.0, angle= 0.0, length=50.0):
        self.difference_distance = 0.0
        self.difference_rotation = 0.0
        self.difference_drift = 0.0
        self.length = length
        self.steer = 0



        #setting coordinates of vehicle
    def set(self, x, y, angle):

        self.x = x
        self.y = y
        self.angle = angle % (2.0 * np.pi)

    def set_difference(self, difference_rotation, difference_distance):
        self.difference_distance = difference_distance
        self.difference_rotation = difference_rotation

    def set_difference_drift(self, drift):
        self.difference_drift = drift

    #steering = angle of front wheel

    def drive(self, steer, distance, tolerance=0.001, max_allowed_steering =np.pi / 4.0):
         if steer > max_allowed_steering:
            steer = max_allowed_steering
         if steer < -max_allowed_steering:
            steer = -max_allowed_steering
         if distance < 0.0:
            distance = 0.0

         steer = random.gauss(steer, self.difference_rotation)
         distance = random.gauss(distance, self.difference_distance)

         steer += self.difference_drift
         

         rotate = np.tan(steer * distance / self.length)
         if abs(rotate) < tolerance:
            
            self.x += distance * np.cos(self.angle)
            self.y += distance * np.sin(self.angle)
            self.angle = (self.angle + rotate) % (2.0 * np.pi)
         else: 
            radius = distance / rotate
            cx = self.x - (np.sin(self.angle) * radius)
            cy = self.y + (np.cos(self.angle) * radius)
            self.angle = (self.angle + rotate) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.angle) * radius)
            self.y = cy - (np.cos(self.angle) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.angle)


class Middle_curve(object):
    def __init__(self):
        self.origin_x = 0
        self.origin_y = 0
        self.x_scaling_factor = 0.00125
        self.y_scaling_factor = 0.00125
        self.total_image_height = 600
        
        
        

    def set(self, pixel_x, pixel_y):

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

    def convert_pixels_to_cartesian(self):
        self.x_mid = (self.pixel_x - self.origin_x) * self.x_scaling_factor
        self.y_mid = (self.total_image_height - self.pixel_y - self.origin_y) * self.y_scaling_factor
        #print("Cartesian Coordinate:", self.x_mid, self.y_mid)
        return self.x_mid, self.y_mid
        

    def update_xymid(self, pixel_x, pixel_y):
        self.x_mid, self.y_mid = self.convert_pixels_to_cartesian(pixel_x, pixel_y)


middle_curve = Middle_curve()
middle_curve.set(800,400)
#middle_curve.set()
middle_curve.x_mid, middle_curve.y_mid = middle_curve.convert_pixels_to_cartesian()

vehicle = Vehicle()
vehicle.set(0, 0.375, 0)
vehicle.set_difference_drift(10/180.*np.pi)  # add drift bias




def calculate_steer():
    # calculate the desired orientation angle from current position to target
    desired_orientation = np.arctan2(middle_curve.y_mid - vehicle.y, middle_curve.x_mid - vehicle.x)
    steer = desired_orientation - vehicle.angle
    # keep the steer angle between -pi and pi
    steer = (steer + np.pi/2) % (2 * np.pi/2) - np.pi/2
    print(steer)
    return steer


def calculate_steer_angle():
    steer_angle = steer * 180/math.pi
    #print("angle", steer_angle)
    return steer_angle

# calculate steer to reach x_mid, y_mid
steer = calculate_steer()
steer_angle = calculate_steer_angle()
# drive the vehicle with the calculated steer and a constant speed
vehicle.drive(steer, 1)

print("Pixel location:", middle_curve.pixel_x, middle_curve.pixel_y)
print("x_mid & y_mid:", middle_curve.x_mid, middle_curve.y_mid)
print("vehicle x&y:", vehicle.x, vehicle.y)
print("steer angle in degrees", steer_angle)