Spirit Level
==============

将X Sense HAT做成一个水平仪。通过读取roll角和pitch角的变化，我们可以判断X Sense HAT当前是否位于水平状态。

TIPS
------

The map block can remap a number from one range to another. If a number is 50，it is at 50% position
of the range of 0~100; then if we map it to the range 0~255 via the map block, the number will be 127.5.

.. image:: img/tip49.png
  :width: 230
  :align: center

逻辑与表达式，如果两个条件都为真，则该表达式的结果为真。

.. image:: img/tip50.png
  :width: 180
  :align: center

使用round块可以约去小数点后的数值，如果小数点第一位小于5，就直接舍去，反之进一位。例如将1.25向下舍入后将变成1。

.. image:: img/tip51.png
  :width: 180
  :align: center

EXAMPLE
---------

.. image:: img/example12.png
  :width: 760
  :align: center










