***************************************
Sprinklers controller (water pump also)
***************************************

.. figure:: ../images/sprinklers.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: sprinklers

.. note::

    * **Node** send sensors values to **Master**
    * **Node** don't take any logical decision
    * **Master** take decision and response Power OFF/ON signal based on settings

.. warning::

    * If **Node** don't update sensors value, **Master** will response Power OFF
    * If **Node** can't communicate with **Master**, will stay in Power OFF
