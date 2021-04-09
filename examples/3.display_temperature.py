from sensor_hat import Bme280
from sensor_hat import RGB_Matrix

__rgb__=RGB_Matrix(0x74)

def forever():
  while True:
    __rgb__.show_text(str('Tem : ') + str(Bme280().read('celsius')),100,'#ffffff')

if __name__ == "__main__":
  forever()