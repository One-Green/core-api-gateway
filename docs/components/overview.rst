********
Overview
********


.. _figure:

.. figure:: ../images/flow.png
   :height: 100
   :width: 200
   :scale: 500
   :align: center
   :alt: flow

   Architecture overview

+--------------------+---------------+----------------+----------------------------+
| Conventional name  | Hardware      | Software       | Purpose                    |
+====================+===============+================+============================+
|                    |               | RaspAp         | Wifi Access point          |
|                    |               +----------------+----------------------------+
|                    |               | Docker         | Container isolation        |
|                    |               |                |                            |
|  Master            |  Raspberry Pi |                | Fast deployment            |
|                    |               +----------------+----------------------------+
|                    |               | Api Gateway    | Unique entry point for     |
|                    |               |                |                            |
|                    |               |                | Nodes communication        |
|                    |               +----------------+----------------------------+
|                    |               | TimescaleDB    | Time series data base      |
|                    |               +----------------+----------------------------+
|                    |               | Grafana        | Data visualisation         |
|                    |               |                |                            |
|                    |               |                | Alert Notification         |
|                    |               +----------------+----------------------------+
|                    |               | Loki           | Light weight Logger        |
|                    |               |                |                            |
|                    |               |                | Grafana native             |
+--------------------+---------------+----------------+----------------------------+
|                    |               | MicroPython    | Convenient way             |
|                    |               |                |                            |
| Nodes              | ESP 32        | PlantKeeper    | develop custom             |
|                    |               |                |                            |
|                    |               | client         | devices                    |
+--------------------+---------------+----------------+----------------------------+
