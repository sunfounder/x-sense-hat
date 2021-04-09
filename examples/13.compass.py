from sensor_hat import RGB_Matrix
import math
from sensor_hat.mpu9250 import MPU9250
from ezblock import I2C

i2c=I2C()
imu = MPU9250(i2c)
imu.start_imu()
__rgb__=RGB_Matrix(0x74)

circle = None
i = None
position = None

circle = [[3,7], [2,7], [1,6], [0,5], [0,4], [0,3], [0,2], [1,1], [2,0], [3,0], [4,0], [5,0], [6,1], [7,2], [7,3], [7,4], [7,5], [6,6], [5,7], [4,7]]

def drawCircle():
  global circle, i, position
  for i in range(1, 21):
    __rgb__.draw_point(circle[int(i - 1)],fill=(51,102,255))


def currentDirection():
  global circle, i, position
  __rgb__.draw_point(circle[-1],fill=(51,255,51))
  __rgb__.draw_point(circle[0],fill=(51,255,51))


def northDrection():
  global circle, i, position
  position = round(imu.magnetic_angle() / 18) % 20
  __rgb__.draw_point(circle[int(position - 1)],fill=(255,0,0))


def forever():
  global circle, i, position
  while True:
    drawCircle()
    currentDirection()
    northDrection()
    __rgb__.display()

if __name__ == "__main__":
  forever()