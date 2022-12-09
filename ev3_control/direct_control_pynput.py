#!/usr/bin/python3

from pynput import keyboard
from ev3_control import Car 

def on_press(key):

    # print('special key {0} pressed'.format(key))
    if key == keyboard.Key.up:          # start forward
        print('\nup pressed')
        car.move(500)
    elif key == keyboard.Key.down:      # start backward 
        print('\ndown pressed')
        car.move(-500)
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

def on_release(key):
    if key == keyboard.Key.up or key ==keyboard.Key.down:            # stop move
            print('\nstop move')
            car.stop()
    if key == keyboard.Key.left or key ==keyboard.Key.right:            # stop turn
            print('\nstop turn')
            car.stop()
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':
    global car
    car = Car()
    # Collect events until released
    with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
        listener.join()
