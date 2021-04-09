import sys
sys.path.append(r'/opt/ezblock')
from Music import *
from sensor_hat.joystick_module import Joystick_Module
from ezblock import constrain
from ezblock import delay

jy = Joystick_Module()

volume = None
volume = 50
background_music('spry.mp3')

def forever():
  global volume
  while True:
    if jy.joystick_motion(motion = 'up') == 1:
      volume = constrain(volume + 5, 0, 100)
    elif jy.joystick_motion(motion = 'down') == 1:
      volume = constrain(volume - 5, 0, 100)
    elif jy.joystick_motion(motion = 'left') == 1:
      music_pause()
    elif jy.joystick_motion(motion = 'right') == 1:
      music_unpause()
    music_set_volume(volume)
    delay(100)

if __name__ == "__main__":
  forever()