
import sys
import rclpy
from rclpy.node import Node
from pynput import keyboard
from std_msgs.msg import String

# Node creation class
class Keyboard_control_pub(Node):

    def __init__(self):
        super().__init__('keyboard_control_publisher')

        # Set default parameters for direct control from keyboard:
        self.message_text = ""
        self.motor_speed = 100      # initial speed when car starts moving
        self.speed_limit = 400      # max reachable speed
        self.speed_step = 20        # speed increased by steps until reach limit
        timer_period = 0.01         # time period for timer

        self.publisher_ = self.create_publisher(String, 'ev3_control_topic', 10)

        self.timer = self.create_timer(timer_period, self.publish_msg)

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()


    def publish_msg(self):
        if self.message_text == "": return
        self.msg = String()
        self.msg.data=self.message_text
        self.publisher_.publish(self.msg)
        print("published message:%s" %self.message_text)
        self.message_text = ""

    # Detecting press of some key on keyboard
    def on_press(self,key):
        if key == keyboard.Key.up:          # start forward
            if (self.motor_speed < self.speed_limit):
                self.motor_speed = self.motor_speed + self.speed_step 
            self.message_text = "move " + str(self.motor_speed)
        elif key == keyboard.Key.down:      # start backward 
            if (self.motor_speed < self.speed_limit): 
                self.motor_speed = self.motor_speed + self.speed_step 
            self.message_text = "move " + str(-self.motor_speed)
        elif key == keyboard.Key.left:      # turn left
            self.message_text = "turn_left"
        elif key == keyboard.Key.right:     # turn right 
            self.message_text = "turn_right"
        elif key == keyboard.Key.enter:     # set current wheel angle to zero 
            self.message_text = "set_zero"
        elif key == keyboard.Key.space:     # stop 
            self.message_text = "stop"

    # Detecting release of some key on keyboard
    def on_release(self,key):
        if key == keyboard.Key.up or key ==keyboard.Key.down:
            self.message_text = "stop"
            self.motor_speed = self.motor_speed
        if key == keyboard.Key.left or key ==keyboard.Key.right:
            self.message_text = "stop_turn"
            self.motor_speed = self.motor_speed
        elif key == keyboard.Key.esc:
            self.message_text = "stop_control"


def main(args=None):

    rclpy.init(args=args)
    keyboard_control_publisher = Keyboard_control_pub()
    rclpy.spin(keyboard_control_publisher)

    keyboard_control_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()