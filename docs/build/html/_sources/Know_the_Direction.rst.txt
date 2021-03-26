Know the Direction
====================

我们把X Sense HAT制作成一个指南针，这样我们就不会迷失方向了。

TIPS
------

绿色箭头表示X Sense HAT检测的方向，你可以通过它来判断当前的位置。

.. image:: img/tip71.png
  :width: 400
  :align: center

这个块读取当前指南针方向，修改下拉选项，可以选择azimuth或者quadrant。

.. image:: img/tip46.png
  :width: 550
  :align: center

EXAMPLE
----------

.. image:: img/example9.png
  :width: 650
  :align: center

azimuth的使用帮助
-----------------

azimuth是从某点的指北方向线起，依顺时针方向到目标方向线之间的水平夹角（指南针的外圈数值）。
根据得出的azimuth，我们就可以知道当前的位置，例如0度就是正北方向，30度就是北偏东30度角方向。

.. image:: img/tip47.png
  :width: 460
  :align: center

quadrant的使用帮助
-------------------

quadrant是将指南针的方向八等分，我们可以借助azimuth来划分这八个区域，例如22.5度和67.5度之间就是NE方向，
而67.5度和112.5度之间就是E方向。

.. image:: img/tip68.jpg
  :width: 530
  :align: center



