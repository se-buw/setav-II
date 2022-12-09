#!/usr/bin/python3

from pynput import keyboard
from ev3_control import move, stop, turn, get_angle, set_zero

def on_press(key):

    # print('special key {0} pressed'.format(key))
    if key == keyboard.Key.up:          # start forward
        print('\nup pressed')
        move(500)
    elif key == keyboard.Key.down:      # start backward 
        print('\ndown pressed')
        move(-500)
    elif key == keyboard.Key.left:      # turn left
        print('\nleft')
        turn("left")
    elif key == keyboard.Key.right:     # turn right 
        print('\nright')
        turn("right")
    elif key == keyboard.Key.ctrl:      # print wheel angle 
        print('\nangle:',get_angle)
    elif key == keyboard.Key.enter:     # set current wheel angle to zero 
        print('\nenter')
        set_zero()
    elif key == keyboard.Key.space:     # stop 
        print('\nspace')
        stop()

def on_release(key):
    if key == keyboard.Key.up or key ==keyboard.Key.down:            # stop move
            print('\nstop move')
            stop()
    if key == keyboard.Key.left or key ==keyboard.Key.right:            # stop turn
            print('\nstop turn')
            stop()
    elif key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
    listener.join()

