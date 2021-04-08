from sensor_hat.mpu9250 import MPU9250
from ezblock import I2C
import math
from sensor_hat import motor_stop
from ezblock import mapping
from sensor_hat import RGB_Matrix
from sensor_hat import motor_power

i2c=I2C()
imu = MPU9250(i2c)
imu.start_imu()
__rgb__=RGB_Matrix(0x74)

threshold = None
x_attitude_angle = None
y_attitude_angle = None
x_axis = None
y_axis = None

threshold = 5

def forever():
  while True:
    global threshold, x_attitude_angle, y_attitude_angle, x_axis, y_axis
    x_attitude_angle = imu.get_posture_angle(aram = "roll")
    y_attitude_angle = imu.get_posture_angle(aram = "pitch")
    if math.fabs(x_attitude_angle) <= threshold and math.fabs(y_attitude_angle) <= threshold:
      motor_stop()
      x_axis = round(mapping(x_attitude_angle, (-threshold), threshold, 0, 6))
      y_axis = round(mapping(y_attitude_angle, threshold, (-threshold), 0, 6))
      __rgb__.clear_screen()
      __rgb__.draw_rectangle([x_axis,y_axis],[x_axis + 1,y_axis + 1],fill=(51,255,51),outline=False)
      __rgb__.display()
    else:
      motor_power(50)

if __name__ == "__main__":
  forever()