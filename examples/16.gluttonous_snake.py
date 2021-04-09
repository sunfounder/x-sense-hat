from sensor_hat.rgb_matrix import RGB_Matrix
import numpy as np
import time 
import random
from sensor_hat.joystick_module import Joystick_Module
 

def run():
    rr = RGB_Matrix(0X74)
    rectangle_start_coor = [0,0]
    rectangle_end_coor = [7,7]
    rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(51,51,0),outline=None, width=0)   #draw a rectangle
    coor_1 = np.asarray([0,2])
    coor_2 = np.asarray([1,2])
    coor_3 = np.asarray([2,2])
    coor_4 = np.asarray([3,2])
    coor_list = [coor_1,coor_2,coor_3,coor_4]
    snake_color = 240 
    jy = Joystick_Module()

    eat_flag = False
    b =  random.randint(1,255)
    g =  random.randint(1,255)
    r =  random.randint(1,255)
    random_coor = [4,4]
    game_time = 20            #set the game time (second)
    game_count = 0
    while True:
        key = jy.joystick_motion_irq()  #获取按键值
        if game_count < 50:   #游戏时间自增上限
            rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(0,51,51),outline=None, width=0)   #draw a rectangle  白天背景
        else:
            rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(0,0,51),outline=None, width=0)   #draw a rectangle   切换晚上黑色背景
        if eat_flag == False:  #绿色点被吃掉，生成新的点
            m = 2
            n = 64
            matrix_list = [[0 for i in range(m)] for j in range(n)]   #生成二维数组
            for i in range(64):
                matrix_list[i][0] = i % 8
                matrix_list[i][1] = int(i / 8)
            coor_list_copy = [list(x) for x in coor_list]   #赋值为8x8的坐标矩阵
            for i in coor_list_copy:   #除去蛇身的点，用剩余的点进行随机生成绿色的点
                matrix_list.remove(i)
            
            random_coor = random.choice(matrix_list)     #随机选择一个点
            eat_flag = True   #标志位控制

        rr.draw_point((random_coor[0],random_coor[1]),fill=(0,255,0))  #画出这个点
        game_count +=1  #游戏时间自增
        
        if key == 'left':  #摇杆往左
            key = 'n'   #清空标志位
            if coor_list[0][0] == coor_list[1][0]:
                for i in range(len(coor_list)-1,0,-1):
                    coor_list[i][1] = coor_list[i-1][1] 
                    coor_list[i][0] = coor_list[i-1][0]

                coor_list[0][0] -= 1
                if coor_list[0][0] < 0:
                    coor_list[0][0] = 7
                        
        elif key == 'down':  #摇杆往上
            key = 'n'    #清空标志位
            if coor_list[0][1] == coor_list[1][1]:
                for i in range(len(coor_list)-1,0,-1):
                    coor_list[i][1] = coor_list[i-1][1] 
                    coor_list[i][0] = coor_list[i-1][0]

                coor_list[0][1] -= 1
                if coor_list[0][1] < 0:
                    coor_list[0][1] = 7


        elif key == 'right':   #摇杆往右
            key = 'n'      #清空标志位
            if coor_list[0][0] == coor_list[1][0]:
                for i in range(len(coor_list)-1,0,-1):
                    coor_list[i][1] = coor_list[i-1][1] 
                    coor_list[i][0] = coor_list[i-1][0]

                coor_list[0][0] += 1
                if coor_list[0][0] > 7:
                    coor_list[0][0] = 0
        elif key == 'up':  #摇杆往下
            key = 'n'    #清空标志位
            if coor_list[0][1] == coor_list[1][1]:
                for i in range(len(coor_list)-1,0,-1):
                    coor_list[i][1] = coor_list[i-1][1] 
                    coor_list[i][0] = coor_list[i-1][0]

                coor_list[0][1] += 1
                if coor_list[0][1] > 7:
                    coor_list[0][1] = 0

        else:  #摇杆无操作，则继续直行
            if coor_list[0][0] == coor_list[1][0]:
                if coor_list[0][1] - coor_list[1][1] == 1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][1] +=1
                    if coor_list[0][1] > 7:
                        coor_list[0][1] = 0
                elif coor_list[0][1] - coor_list[1][1] == -1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][1] -=1
                    if coor_list[0][1] < 0:
                        coor_list[0][1] = 7
                
                elif coor_list[0][1] - coor_list[1][1] > 1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][1] -=1
                    if coor_list[0][1] < 0:
                        coor_list[0][1] = 7

                elif coor_list[0][1] - coor_list[1][1] < -1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][1] +=1
                    if coor_list[0][1] > 7:
                        coor_list[0][1] = 0
                # break
            if coor_list[0][1] == coor_list[1][1]:

                if coor_list[0][0] - coor_list[1][0] == 1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][0] +=1
                    if coor_list[0][0] > 7:
                        coor_list[0][0] = 0
                elif coor_list[0][0] - coor_list[1][0] == -1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][0] -=1
                    if coor_list[0][0] < 0:
                        coor_list[0][0] = 7
                
                elif coor_list[0][0] - coor_list[1][0] > 1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][0] -=1
                    if coor_list[0][0] < 0:
                        coor_list[0][0] = 7

                elif coor_list[0][0] - coor_list[1][0] < -1:
                    for i in range(len(coor_list)-1,0,-1):
                        coor_list[i][1] = coor_list[i-1][1] 
                        coor_list[i][0] = coor_list[i-1][0]
                    coor_list[0][0] +=1
                    if coor_list[0][0] > 7:
                        coor_list[0][0] = 0


        if coor_list[0][0] == random_coor[0] and coor_list[0][1] == random_coor[1]:  # 蛇吃到绿色的点
            eat_flag =False
            if coor_list[-1][0] == coor_list[-2][0]:
                if coor_list[-1][1] > coor_list[-2][1]:
                    new_x = coor_list[-1][0]
                    new_y = coor_list[-1][1] + 1
                    if new_y > 7:
                        new_y = 0
                elif coor_list[-1][1] < coor_list[-2][1]:
                    new_x = coor_list[-1][0]
                    new_y = coor_list[-1][1] - 1
                    if new_y < 0:
                        new_y = 7
                coor_list.append([new_x,new_y])

            elif coor_list[-1][1] == coor_list[-2][1]:
                if coor_list[-1][0] > coor_list[-2][0]:
                    new_x = coor_list[-1][0] + 1
                    new_y = coor_list[-1][1]
                    if new_x > 7:
                        new_x = 0
                elif coor_list[-1][0] < coor_list[-2][0]:
                    new_x = coor_list[-1][0] - 1
                    new_y = coor_list[-1][1]
                    if new_x < 0:
                        new_x = 7
                coor_list.append([new_x,new_y])  

        for i in range(len(coor_list)-1,0,-1):   #判断是否咬到自己的身体
            if (coor_list[0]  == coor_list[i]).all():
                coor_list = [coor_1,coor_2,coor_3,coor_4]
                break
        coor_list_lenth = len(coor_list)
        for i in range(coor_list_lenth):
            rr.draw_point(tuple(coor_list[i]),fill=(int(240/(i+1)),0,0))

        if game_count >= game_time*5:
            rr.draw_rectangle(rectangle_start_coor,rectangle_end_coor,fill=(51,51,51),outline=None, width=0) 
            for i in range(2):
                rr.show_text("Score: %s"%(len(coor_list)-4),100,(51,51,51))
                time.sleep(0.5)
            game_count = 0
            coor_list = [coor_1,coor_2,coor_3,coor_4]

        rr.display()
        time.sleep(0.2)


if __name__ == "__main__":

    run()
    while True:
        pass
 

