from sensor_hat.mpu9250 import MPU9250
from ezblock import I2C
from ezblock import print
from ezblock import delay

i2c=I2C()
imu = MPU9250(i2c)
imu.start_imu()

def forever():
  while True:
    print("%s"%(imu.read("accel","x")))
    delay(100)

if __name__ == "__main__":
  forever()