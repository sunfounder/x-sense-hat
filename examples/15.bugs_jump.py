import sys
import tty
import termios
import asyncio
from sensor_hat.joystick_module import Joystick_Module
from sensor_hat.rgb_matrix import RGB_Matrix
import numpy as np
import time 
import threading
import random


def bugs_jump():
    rr = RGB_Matrix(0X74)
    i = 0
    rectangle_start_coor = [0,0]
    rectangle_end_coor = [7,7]
    jy = Joystick_Module()
    chon_y = 7
    b_list = []
    bone_flag = True
    point_val = 0
    while True:
        key = jy.joystick_motion_irq()

        rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(0,0,0),outline=None, width=0)
        if i % 7 == 0 and bone_flag == True:  #判断是否越过障碍或一轮时间是否到了
            b_length =  random.randint(0,1)
            game_time =  random.randint(4,10)
            count_time = 0
        
        if b_length > 0: #是否生产身体
            
            bone_flag = False
            rr.draw_line([7-count_time,0],[7-count_time,b_length],fill=(255,165,0))
            count_time += 1
            if count_time > 7:
                point_val += 1
                bone_flag = True
            
        if key == 'up':  #摇杆是否有往上操作
            chon_y = 3
            rr.draw_line([0,chon_y],[1,chon_y],fill=(0,51,0))
            rr.draw_point([2,chon_y],fill=(51,0,0))
            
        else:
            chon_y = 0
            if i % 2 == 0:
                rr.draw_point([1,chon_y],fill=(0,51,0))
            else:
                rr.draw_point([1,chon_y+1],fill=(0,51,0))
            rr.draw_point([0,chon_y],fill=(0,51,0))
            rr.draw_point([2,chon_y],fill=(51,0,0))

            if 7-count_time == 1:  
                # print("fail")
                rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(0,0,0),outline=None, width=0)
                rr.draw_point([1,chon_y],fill=(51,0,0))
                rr.draw_point([2,chon_y],fill=(51,0,0))
                rr.draw_point([0,chon_y],fill=(51,0,0))

                rr.display()
                time.sleep(2)
                rr.show_text(point_val, delay=500,color=(0,15,0))
                point_val = 0
                count_time = 0
                b_length =0
                bone_flag = True

        rr.display()
        time.sleep(float(1/game_time))
        i+=1

        if i > 7:
            i = 0


if __name__ == "__main__":

    bugs_jump()
    # while True:
    #     pass
 

