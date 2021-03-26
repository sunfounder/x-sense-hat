Gravity Ball Game
===================

接下来我们在X Sense HAT上制作一个重力小球的游戏。按下摇杆后，游戏开始。如果RGB点阵屏上的小球碰到边缘，则游戏结束。

TIPS
-----

使用这个块来创建一个新的循环语句。

.. image:: img/tip52.png
  :width: 350
  :align: center

中断最近的一次循环，但是不能退出Forever语句的循环。

.. image:: img/tip53.png
  :width: 280
  :align: center

Here, we also use to do something block to create a new funtion, but the block does not return any value.

.. image:: img/tip54.png
  :width: 380
  :align: center

EXAMPLE
---------

.. image:: img/example13.png
  :width: 800
  :align: center

拓展
-----

我们当前代码是以递增坐标值的方式处理小球移动的轨迹变化，如果你想在X Sense HAT上模拟真实重力感应的小球，你可以使用
S = 1/2 * a * t^2这条公式来计算小球在不同轴上的移动距离，例如我们读取到X Sense HAT在X轴上的加速度为a1，
在Y轴上的加速度为a2。那么在t1时间内，X Sense HAT在X轴上位移了S1（1/2 * a1 * t1^2），
在Y轴上位移了S2（1/2 * a2 * t1^2）。假设小球的原坐标为（x1，y1），那么在t1时间后，它的坐标就变化为
（x1+S1，y1+S2）。

你可以尝试地编写这段代码，将小球随着加速度的变化而移动会让这个实验变得更有趣。






