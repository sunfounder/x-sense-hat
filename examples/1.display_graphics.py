from sensor_hat import RGB_Matrix
from ezblock import delay

__rgb__=RGB_Matrix(0x74)

def forever():
  while True:
    __rgb__.draw_shape(["#000000","#000000","#ff0000","#ff0000","#ff0000","#000000","#000000","#000000",
                        "#ff0000","#ff0000","#ff0000","#ffcc33","#ffcc33","#ff0000","#000000","#000000",
                        "#000000","#ff6600","#ff6600","#ffffff","#ff6600","#ffffff","#000000","#000000",
                        "#000000","#000000","#ff6600","#ff6600","#ff6600","#ff6600","#000000","#000000",
                        "#000000","#ff6600","#ff0000","#ff0000","#ff0000","#ff0000","#ff6600","#000000",
                        "#000000","#ff6600","#ff0000","#ff0000","#ff0000","#ff0000","#ff6600","#000000",
                        "#000000","#000000","#3333ff","#3333ff","#3333ff","#3333ff","#000000","#000000",
                        "#000000","#000000","#3333ff","#000000","#000000","#3333ff","#000000","#000000"])
    delay(1000)
    __rgb__.show_icon("heart",(255,0,0))
    delay(1000)

if __name__ == "__main__":
  forever()
