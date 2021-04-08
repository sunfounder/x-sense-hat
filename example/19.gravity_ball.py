import time
from ezblock import I2C, Pin
from sensor_hat.mpu9250 import MPU9250
import math
import random
import smbus2
from sensor_hat.rgb_matrix import RGB_Matrix
from sensor_hat.vibrating_motor import *

i2c = I2C()
sensor = MPU9250(i2c)
sensor.start_imu()
width = 8
height = 8
rr = RGB_Matrix(0X74)


def run():
    color = (10,0,10)
    coor_1 = [4,4]
    coor_2 = [3,3]
    scale = 0.2
    random_coor = [6,6]
    random_color = [0,20,20]
    eat_flag = True
    point_val = 0
    time_count = 0
    color_dict = {0:(50,10,0),1:(10,75,0),2:(35,0,150)}
    while True:
        time_count+=1
        if eat_flag == True:
            random_x_list = [i for i in range(8)]
            random_x_list.remove(coor_1[0])
            random_x_list.remove(coor_2[0])
            random_y_list = [i for i in range(8)]
            random_y_list.remove(coor_1[1])
            random_y_list.remove(coor_2[1])
            random_coor[0] = random.choice(random_x_list)
            random_coor[1] = random.choice(random_y_list)
            
            random_color[0] = random.randint(1,50)
            random_color[1]= random.randint(1,50)
            random_color[2] = random.randint(1,50)
            eat_flag = False

        if sensor.read("accel","y") >=scale:
            coor_1[1]+=1
            coor_2[1]+=1
            if coor_1[1] > 7 or coor_2[1] > 7:
                coor_1[1] = 7
                coor_2[1] = 6
                color = (0,0,20)
                point_val-=1
                motor_power(100)
            else:
                color = (10,10,0)
                motor_stop()
        elif sensor.read("accel","y") <= -scale:
            coor_2[1]-=1
            coor_1[1]-=1
            if coor_2[1] < 0 or coor_1[1] < 0:
                coor_2[1] = 0
                coor_1[1] = 1
                color = (0,0,20)
                point_val-=1
                motor_power(100)
            else:
                color = (10,10,0)
                motor_stop()
        if sensor.read("accel","x") <=-scale:
            coor_1[0]-=1
            coor_2[0]-=1
            if coor_1[0] < 0 or coor_2[0] < 0:
                coor_1[0] = 0
                coor_2[0] = 1
                color = (0,0,20)
                point_val-=1
                motor_power(100)
            else:
                color = (10,10,0)
                motor_stop()

        elif sensor.read("accel","x") >=scale:
            coor_2[0]+=1
            coor_1[0]+=1
            if coor_2[0] > 7 or coor_1[0] > 7:
                coor_2[0] = 7
                coor_1[0] = 6
                color = (0,0,20)
                point_val-=1
                motor_power(100)
            else:
                color = (10,10,0)
                motor_stop()

        if random_coor[0] == coor_2[0] or random_coor[0] == coor_1[0]:
            if random_coor[1] == coor_2[1] or random_coor[1] == coor_1[1]:
                eat_flag =True
                point_val+=1

        rr.draw_point((random_coor[0],random_coor[1]),fill=tuple(random_color))  
        if color == (0,0,20):
            rr.draw_rectangle([coor_1[0],coor_1[1]],[coor_2[0],coor_2[1]], fill=color)
        else:
            rr.draw_rectangle([coor_1[0],coor_1[1]],[coor_2[0],coor_2[1]], fill=color_dict[int(time_count/40)])
        rr.display()
        time.sleep(0.1)

        rr.draw_rectangle([0,0],[width,height], outline=0, fill=0)
        if time_count >=119:
            break
            rr.draw_rectangle([0,0],[width,height], outline=0, fill=0)
            rr.display()
    motor_stop()
    rr.show_text("Score: %s"%point_val,delay=200)

if __name__ == "__main__":
    run()
