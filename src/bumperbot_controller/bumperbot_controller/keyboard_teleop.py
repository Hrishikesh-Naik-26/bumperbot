#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from pynput import keyboard

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__("Keyboard_Teleop")

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.target_linear_velocity = 0.0
        self.target_angular_velocity = 0.0
        self.linear_velocity_delta = 0.01
        self.angular_velocity_delta = 0.01

        self.velocity_timer_ = self.create_timer(0.05, self.publish_velocity)

        self.teleop_publisher_ = self.create_publisher(TwistStamped, "bumperbot_controller/cmd_vel", 10)
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )    

    def on_press(self, key):

        if hasattr(key, 'char'):
            key = key.char
            match key:
                case 'w':
                    self.target_linear_velocity = 0.2

                case 's':
                    self.target_linear_velocity = -0.2

                case 'a':
                    self.target_angular_velocity = 0.5

                case 'd':
                    self.target_angular_velocity = -0.5

                case 'q':
                    rclpy.shutdown()

                case _:
                    pass

        print(f"Pressed: {key}")

    def on_release(self, key):
        if hasattr(key, 'char'):
            key = key.char
            match key:
                case 'w':
                    self.target_linear_velocity = 0.0

                case 's':
                    self.target_linear_velocity = 0.0

                case 'a':
                    self.target_angular_velocity = 0.0

                case 'd':
                    self.target_angular_velocity = 0.0

                case _:
                    pass

        print(f"Released: {key}")

    def publish_velocity(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()

        if (self.linear_velocity < self.target_linear_velocity):
            self.linear_velocity += self.linear_velocity_delta
            if (abs(self.target_linear_velocity - self.linear_velocity) <= self.linear_velocity_delta):
                self.linear_velocity = self.target_linear_velocity
        elif(self.linear_velocity > self.target_linear_velocity):
            self.linear_velocity -= self.linear_velocity_delta
            if (abs(self.target_linear_velocity - self.linear_velocity) <= self.linear_velocity_delta):
                self.linear_velocity = self.target_linear_velocity
        else:
            self.linear_velocity = self.target_linear_velocity

        if (self.angular_velocity < self.target_angular_velocity):
            self.angular_velocity += self.angular_velocity_delta
            if (abs(self.target_angular_velocity - self.angular_velocity) <= self.angular_velocity_delta):
                self.angular_velocity = self.target_angular_velocity
        elif (self.angular_velocity > self.target_angular_velocity):
            self.angular_velocity -= self.angular_velocity_delta
            if (abs(self.target_angular_velocity - self.angular_velocity) <= self.angular_velocity_delta):
                self.angular_velocity = self.target_angular_velocity
        else:
            self.angular_velocity = self.target_angular_velocity
            
        msg.twist.linear.x = self.linear_velocity
        msg.twist.angular.z = self.angular_velocity

        self.teleop_publisher_.publish(msg)

def main():
    rclpy.init()
    keyboard_teleoperation = KeyboardTeleop()
    keyboard_teleoperation.listener.start()
    rclpy.spin(keyboard_teleoperation)
    keyboard_teleoperation.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()

                        
                    

