from sensor_hat import RGB_Matrix
from ezblock import delay

__rgb__=RGB_Matrix(0x74)   
    
def forever():
  while True:
    __rgb__.clear_screen()
    __rgb__.draw_point([1,1],fill=(51,255,51))
    __rgb__.display()
    delay(1000)
    __rgb__.clear_screen()
    __rgb__.draw_line([1,1],[6,1],fill=(51,255,51))
    __rgb__.display()
    delay(1000)
    __rgb__.clear_screen()
    __rgb__.draw_rectangle([1,1],[6,6],fill=(51,255,51),outline=True)
    __rgb__.display()
    delay(1000)
    __rgb__.clear_screen()
    __rgb__.draw_rectangle([1,1],[6,6],fill=(51,255,51),outline=False)
    __rgb__.display()
    delay(1000)
    __rgb__.clear_screen()
    __rgb__.draw_ellipse([3,3],2,fill=(51,255,51))
    __rgb__.display()
    delay(1000)

if __name__ == "__main__":
  forever()