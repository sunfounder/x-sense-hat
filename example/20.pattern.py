from os import system
import smbus2
import bme280
from sensor_hat.rgb_matrix import RGB_Matrix
import time


width = 8
height = 8


rr = RGB_Matrix(0X74) 

def hsb2rgb(hsb):
    '''
    Transforms a hsb array to the corresponding rgb tuple
    In: hsb = array of three ints (h between 0 and 360, s and v between 0 and 100)
    Out: rgb = array of three ints (between 0 and 255)
    '''
    H = float(hsb[0] / 360.0)
    S = float(hsb[1] / 100.0)
    B = float(hsb[2] / 100.0)

    if (S == 0):
        R = int(round(B * 255))
        G = int(round(B * 255))
        B = int(round(B * 255))
    else:
        var_h = H * 6
        if (var_h == 6):
            var_h = 0  # H must be < 1
        var_i = int(var_h)
        var_1 = B * (1 - S)
        var_2 = B * (1 - S * (var_h - var_i))
        var_3 = B * (1 - S * (1 - (var_h - var_i)))

        if      (var_i == 0):
            var_r = B     ; var_g = var_3 ; var_b = var_1
        elif (var_i == 1):
            var_r = var_2 ; var_g = B     ; var_b = var_1
        elif (var_i == 2):
            var_r = var_1 ; var_g = B     ; var_b = var_3
        elif (var_i == 3):
            var_r = var_1 ; var_g = var_2 ; var_b = B
        elif (var_i == 4):
            var_r = var_3 ; var_g = var_1 ; var_b = B
        else:
            var_r = B     ; var_g = var_1 ; var_b = var_2

        R = int(round(var_r * 255)*0.1)
        G = int(round(var_g * 255)*0.1)
        B = int(round(var_b * 255)*0.1)

    return (R, G, B)

flag = True

def run():
    global flag
    flag = True
    coor = [0,0]
    time_delay = 0.01
    a = 0
    b = 0
    color = (25,25,25)
    colorHSV_list = [0,150,150]
    for i in range(7,0,-1):
        for len_num in range(4):
            if not flag:
                break
            if len_num  == 0:
                for k in range(7-i,i):
                    colorHSV_list[0]+=5.5
                    coor[1] = k
                    coor[0] = 7-i
                    rr.draw_point((coor[0],coor[1]),fill=hsb2rgb(colorHSV_list))
                    rr.display()
                    time.sleep(time_delay)
            elif len_num == 1:
                for k in range(7-i,i):
                    colorHSV_list[0]+=5.5
                    coor[1] = i
                    coor[0] = k
                    rr.draw_point((coor[0],coor[1]),fill=hsb2rgb(colorHSV_list))
                    rr.display()
                    time.sleep(time_delay)
            elif len_num == 2:
                for k in range(7-i,i):
                    colorHSV_list[0]+=5.5
                    coor[1] = 7-k
                    coor[0] = i
                    rr.draw_point((coor[0],coor[1]),fill=hsb2rgb(colorHSV_list))
                    rr.display()
                    time.sleep(time_delay)
            elif len_num == 3:
                for k in range(7-i,i):
                    colorHSV_list[0]+=5.5
                    coor[1] = 7-i
                    coor[0] = 7-k
                    rr.draw_point((coor[0],coor[1]),fill=hsb2rgb(colorHSV_list))
                    rr.display()
                    time.sleep(time_delay)

if __name__ == "__main__":
    run()

