Test the Vibration Motor
===========================

我们可以用蓝牙界面的滑条来控制X Sense HAT上的电机的振动频率。

TIPS
------

To use the remote control function, you need to enter the Bluetooth control page from the left side of 
main page.

.. image:: img/tip4.png
  :width: 250
  :align: center

Here we drag a Slider from the Bluetooth contro page to 控制振动电机的振动频率。

.. image:: img/tip5.png
  :width: 160
  :align: center

To enable the remote control, you need to add read from remote block in the first line of the Forever 
  block.

.. image:: img/tip6.png
  :width: 200
  :align: center

This block reads the Slider value in the Bluetooth control page.

.. image:: img/tip7.png
  :width: 225
  :align: center

Adjust 振动电机的振动频率 in the range “0 ~ 100”.

.. image:: img/tip8.png
  :width: 180
  :align: center

EXAMPLE
---------

.. image:: img/example2.png
  :width: 680
  :align: center

