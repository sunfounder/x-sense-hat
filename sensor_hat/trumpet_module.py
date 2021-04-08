from ezblock.tts import TTS
import time

# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont
from os import system



class Trumpet_Module(object):

    def __init__(self):
        self.tts = TTS()
        self.flag = True
        self.status = 0
        # self.words = ["Hello", "Hi", "Good bye", "Nice to meet you"]

    def speak(self,words = 'Hello'):
        self.tts.say(words)

if __name__=="__main__":
    import time
    tm = Trumpet_Module()
    while True:
        tm.speak("hello sir")
        time.sleep(2)
        tm.speak("nice to meet you")
        time.sleep(2)
        system("sudo mplayer wo.mp3 </dev/null >/dev/null 2>&1 &")
    system("sudo killall alpay")


