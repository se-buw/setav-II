#!/usr/bin/python3

from pynput import keyboard
from ev3_control import Car 
<<<<<<< HEAD
motor_speed = 100
def on_press(key):
    global motor_speed
    if key == keyboard.Key.up:          # start forward
        print('\nup pressed')
        if (motor_speed<700): motor_speed = motor_speed+50 
        car.move(motor_speed)
    elif key == keyboard.Key.down:      # start backward 
        print('\ndown pressed')
        if (motor_speed<700): motor_speed = motor_speed+50
        car.move(-motor_speed)
=======

def on_press(key):

    # print('special key {0} pressed'.format(key))
    if key == keyboard.Key.up:          # start forward
        print('\nup pressed')
        car.move(500)
    elif key == keyboard.Key.down:      # start backward 
        print('\ndown pressed')
        car.move(-500)
>>>>>>> 8dd8084dbde1b064ab26b23311b6b7df3bb52e96
    elif key == keyboard.Key.left:      # turn left
        print('\nleft')
        car.turn("left")
    elif key == keyboard.Key.right:     # turn right 
        print('\nright')
        car.turn("right")
    elif key == keyboard.Key.ctrl:      # print wheel angle 
        print('\nangle:',car.get_angle)
    elif key == keyboard.Key.enter:     # set current wheel angle to zero 
        print('\nenter')
        car.set_zero()
    elif key == keyboard.Key.space:     # stop 
        print('\nspace')
        car.stop()
<<<<<<< HEAD
        motor_speed

def on_release(key):
    global motor_speed
    if key == keyboard.Key.up or key ==keyboard.Key.down:            # stop move
            print('\nstop move')
            car.stop()
            motor_speed = 100
    if key == keyboard.Key.left or key ==keyboard.Key.right:            # stop turn
            print('\nstop turn')
            car.stop()
            motor_speed = 100
=======

def on_release(key):
    if key == keyboard.Key.up or key ==keyboard.Key.down:            # stop move
            print('\nstop move')
            car.stop()
    if key == keyboard.Key.left or key ==keyboard.Key.right:            # stop turn
            print('\nstop turn')
            car.stop()
>>>>>>> 8dd8084dbde1b064ab26b23311b6b7df3bb52e96
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':
    global car
    car = Car()
    # Collect events until released
    with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
        listener.join()
