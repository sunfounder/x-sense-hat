import sys
sys.path.append(r'/opt/ezblock')
from sensor_hat import RGB_Matrix
from sensor_hat.joystick_module import Joystick_Module
from ezblock import constrain
from ezblock import delay
from sensor_hat import motor_power
from sensor_hat import motor_stop
from sensor_hat import Bme280
from Music import *

jy = Joystick_Module()
__rgb__=RGB_Matrix(0x74)

x_coor = None
y_coor = None
play_status = None

def Initialisation():
  global x_coor, y_coor, play_status
  __rgb__.clear_screen()
  __rgb__.draw_point([1,6],fill=(51,255,51))
  __rgb__.draw_line([5,6],[6,6],fill=(51,255,51))
  __rgb__.draw_line([1,2],[2,2],fill=(51,255,51))
  __rgb__.draw_point([1,1],fill=(51,255,51))
  __rgb__.draw_rectangle([5,2],[6,1],fill=(51,255,51),outline=False)

x_coor = 0
y_coor = 4
play_status = 'stop'


def motorVibration():
  global x_coor, y_coor, play_status
  motor_power(50)
  delay(1000)
  motor_stop()


def displayTem():
  global x_coor, y_coor, play_status
  __rgb__.show_text(str('Tem:') + str(Bme280().read('celsius')),100,'#ff0000')


def playMusic():
  global x_coor, y_coor, play_status
  if play_status == 'stop':
    play_status = 'start'
    background_music('spry.mp3')
  elif play_status == 'start':
    play_status = 'stop'
    music_stop()


def drawGraphic():
  global x_coor, y_coor, play_status
  __rgb__.show_icon("heart",(255,0,0))
  delay(2000)


def forever():
  global x_coor, y_coor, play_status
  while True:
    Initialisation()
    if jy.joystick_motion(motion = 'up') == 1:
      y_coor = constrain(y_coor + 4, 0, 4)
    elif jy.joystick_motion(motion = 'down') == 1:
      y_coor = constrain(y_coor - 4, 0, 4)
    elif jy.joystick_motion(motion = 'left') == 1:
      x_coor = constrain(x_coor - 4, 0, 4)
    elif jy.joystick_motion(motion = 'right') == 1:
      x_coor = constrain(x_coor + 4, 0, 4)
    elif jy.joystick_motion(motion = 'press') == 1:
      __rgb__.clear_screen()
      if x_coor == 0 and y_coor == 4:
        motorVibration()
      elif x_coor == 4 and y_coor == 4:
        displayTem()
      elif x_coor == 0 and y_coor == 0:
        playMusic()
      elif x_coor == 4 and y_coor == 0:
        drawGraphic()
      delay(500)
    __rgb__.draw_rectangle([x_coor,y_coor],[x_coor + 3,y_coor + 3],fill=(51,102,255),outline=True)
    __rgb__.display()

if __name__ == "__main__":
  forever()