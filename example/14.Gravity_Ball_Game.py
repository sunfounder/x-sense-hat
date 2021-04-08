from sensor_hat.joystick_module import Joystick_Module
jy = Joystick_Module()
from sensor_hat.mpu9250 import MPU9250
from ezblock import I2C
from sensor_hat import motor_power
from ezblock import delay
from sensor_hat import motor_stop
from sensor_hat import RGB_Matrix

i2c=I2C()
imu = MPU9250(i2c)
imu.start_imu()
__rgb__=RGB_Matrix(0x74)

ball_move_speed = None
x_coor = None
y_coor = None
x_accel = None
y_accel = None

ball_move_speed = 0.1

def movingBall():
  global ball_move_speed, x_coor, y_coor, x_accel, y_accel
  if x_accel > 0 and y_accel > 0:
    x_coor = x_coor + ball_move_speed
    y_coor = y_coor + ball_move_speed
  elif x_accel < 0 and y_accel < 0:
    x_coor = x_coor - ball_move_speed
    y_coor = y_coor - ball_move_speed
  elif x_accel > 0 and y_accel < 0:
    x_coor = x_coor + ball_move_speed
    y_coor = y_coor - ball_move_speed
  elif x_accel < 0 and y_accel > 0:
    x_coor = x_coor - ball_move_speed
    y_coor = y_coor + ball_move_speed

def gameOver():
  global ball_move_speed, x_coor, y_coor, x_accel, y_accel
  __rgb__.show_text('GAME OVER',50,'#ff0000')
  __rgb__.clear_screen()
  __rgb__.display()


def forever():
  global ball_move_speed, x_coor, y_coor, x_accel, y_accel
  x_coor = 3
  y_coor = 3
  while True:
    if jy.joystick_motion(motion = 'press') == 1:
      while True:
        x_accel = imu.read("accel","x")
        y_accel = imu.read("accel","y")
        movingBall()
        if x_coor < 0 or x_coor > 8 or y_coor < 0 or y_coor > 8:
          motor_power(50)
          delay(1000)
          motor_stop()
          break
        __rgb__.clear_screen()
        __rgb__.draw_point([x_coor,y_coor],fill=(51,255,51))
        __rgb__.display()
      gameOver()

if __name__ == "__main__":
  forever()