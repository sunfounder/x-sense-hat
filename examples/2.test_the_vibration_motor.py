from sensor_hat import motor_power
from ezblock import delay

i = None

def forever():
  while True:
    global i
    for i in range(1, 100):
      motor_power(i)
      delay(50)
    delay(2000)

if __name__ == "__main__":
  forever()