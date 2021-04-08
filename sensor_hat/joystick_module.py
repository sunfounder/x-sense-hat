#!/usr/bin/python3
"""This is the module docstring."""
import time
from gpiozero import Button



class Joystick_Module(object):

    FREE = 'free'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    PRESS = 'press'

    def __init__(self):
        self.joystick_motion_flag = 'free'

        self.joystick_up = Button(17)
        self.joystick_right = Button(23)
        self.joystick_down = Button(27)
        self.joystick_left = Button(6)
        self.joystick_press = Button(26)

        self.joystick_up.when_pressed = self.joystick_up_handle
        self.joystick_down.when_pressed = self.joystick_down_handle
        self.joystick_left.when_pressed = self.joystick_left_handle
        self.joystick_right.when_pressed = self.joystick_right_handle
        self.joystick_press.when_pressed = self.joystick_press_handle

    def joystick_left_handle(self):
        self.joystick_motion_flag = 'left'

    def joystick_right_handle(self):
        self.joystick_motion_flag = 'right'

    def joystick_up_handle(self):
        self.joystick_motion_flag = 'up'

    def joystick_down_handle(self):
        self.joystick_motion_flag = 'down'

    def joystick_press_handle(self):
        self.joystick_motion_flag = 'press'

    def joystick_motion(self,motion = "up"):
        if motion == "up":
            return self.joystick_up.value
        elif motion == "down":
                return self.joystick_down.value
        elif motion == "left":
                return self.joystick_left.value
        elif motion == "right":
                return self.joystick_right.value
        elif motion == "press":
                return self.joystick_press.value
        else:
            raise Exception("parameter error!")

    def joystick_motion_irq(self):
        if self.joystick_motion_flag == 'up':
            # print('up')
            self.joystick_motion_flag = 'free'
            return self.UP
        elif self.joystick_motion_flag == 'down':
            # print('down')
            self.joystick_motion_flag = 'free'
            return self.DOWN
        elif self.joystick_motion_flag == 'left':
            # print('left')
            self.joystick_motion_flag = 'free'
            return self.LEFT
        elif self.joystick_motion_flag == 'right':
            # print('right')
            self.joystick_motion_flag = 'free'
            return self.RIGHT
        elif self.joystick_motion_flag == 'press':
            # print('press')
            self.joystick_motion_flag = 'free'
            return self.PRESS
        else:
            # self.joystick_motion_flag = 'free'
            return self.FREE


if __name__=="__main__":
    # jy = Joystick_Module()
    # while True:
    #     button_type = jy.joystick_motion_irq()
    #     if  button_type != 'free':
    #         print(button_type)
    #     time.sleep(0.01)
    jy = Joystick_Module()
    while True:
        button_type = jy.joystick_motion('up')
        if  button_type != 'free':
            print(button_type)
        time.sleep(0.01)



