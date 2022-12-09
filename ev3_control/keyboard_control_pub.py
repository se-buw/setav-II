#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from pynput import keyboard
from std_msgs.msg import String


class Keyboard_control_pub(Node):

    def __init__(self):
        super().__init__('keyboard_control_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        # Collect events until released
        with keyboard.Listener( on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publ: "%s"' % msg.data)
        self.i += 1

    def on_press(key,self):
        print("sssaa")
        msg = String()
        if key == keyboard.Key.up:          # start forward
            print('\nup pressed')
            msg.data = 'up pressed'
            self.publisher_.publish(msg)
            self.get_logger().info('Publ: "%s"' % msg.data)
        elif key == keyboard.Key.down:      # start backward 
            print('\ndown pressed')
        elif key == keyboard.Key.left:      # turn left
            print('\nleft')
        elif key == keyboard.Key.right:     # turn right 
            print('\nright')
        elif key == keyboard.Key.ctrl:      # print wheel angle 
            print('\nctrl')
        elif key == keyboard.Key.enter:     # set current wheel angle to zero 
            print('\nenter')
        elif key == keyboard.Key.space:     # stop 
            print('\nspace')

    def on_release(key,self):
        if key == keyboard.Key.up or key ==keyboard.Key.down:            # stop move
                print('\nstop move')
        if key == keyboard.Key.left or key ==keyboard.Key.right:         # stop turn
                print('\nstop turn')
        elif key == keyboard.Key.esc:
            # Stop listener
            return False


def main(args=None):
    rclpy.init(args=args)

    keyboard_control_publisher = Keyboard_control_pub()

    rclpy.spin(keyboard_control_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    keyboard_control_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()