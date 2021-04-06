# import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
  
p = GPIO.PWM(24, 1000)  # 通道为 12 频率为 50Hz


def motor_power(value):


    try:
        p.start(value)
    except:
        print("clean GPIO")
        GPIO.cleanup()
    

def motor_stop():
    p.start(0)


if __name__ == '__main__':
    import time
    while True:
        motor_power(100)
        time.sleep(3)
        motor_stop()
        time.sleep(0.5)
