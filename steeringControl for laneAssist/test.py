import random
import numpy as np
import matplotlib.pyplot as plt


class Vehicle(object):

    #intialial position of vehicle
    def _init_(self, x=0.0, y=0.0, angle= 0.0, length=50.0):
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
         print(steer)

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

    def _repr_(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.angle)


class Middle_curve(object):
    def __init__(self, pixel_x = 0, pixel_y = 0):
        self.origin_x = 0
        self.origin_y = 0
        self.x_scaling_factor = 0.00125
        self.y_scaling_factor = 0.00125
        self.total_image_height = 600
        
        

    def set(self, pixel_x, pixel_y):

        self.pixel_x = pixel_x
        self.pixel_y = pixel_y

    def convert_pixels_to_cartesian(self, pixel_x, pixel_y):
        self.x_mid = (self.pixel_x - self.origin_x) * self.x_scaling_factor
        self.y_mid = (self.total_image_height - self.pixel_y - self.origin_y) * self.y_scaling_factor
        #print("Cartesian Coordinate:", x_mid, y_mid)
        return self.x_mid, self.y_mid
        

    def update_xymid(self, pixel_x, pixel_y):
        self.x_mid, self.y_mid = self.convert_pixels_to_cartesian(pixel_x, pixel_y)


pixel_x = 400
pixel_y = 550
middle_curve = Middle_curve()
middle_curve.set(400, 550)



x, y = middle_curve.convert_pixels_to_cartesian(pixel_x, pixel_y)

print("Pixel location:", pixel_x, pixel_y)
print("Cartesian Coordinate:", middle_curve.x_mid, middle_curve.y_mid)


vehicle = Vehicle()
vehicle.set(0, 0.375, 0)
vehicle.set_difference_drift(10/180.*np.pi)  # add drift bias
print("vehicle x&y:", vehicle.x, vehicle.y)