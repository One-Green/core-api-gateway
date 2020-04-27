.. plant keeper documentation master file, created by
   sphinx-quickstart on Thu Apr 23 22:18:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to plant keeper's documentation!
========================================

This project provides a complete framework for plant cultivation both indoors and outdoors.

Master
------

The framework is composed of a **Master** including functionalities such as:

- API Gateway for data digestion (written in Python/Django)

- Graphical interface to configure the components (Django admin interface -- future is Angular webapp !)

- Interface for monitoring and alert management (Grafana)

- Controllers to ensure to send good signal to activated, deactivate valve, pump etc ...


Nodes
-----

The second part of framework is **Node** ESP32 MicroPython Client class

Repository : https://github.com/shanisma/pk-node-client

Import client, select Node Type (sprinkler, water pump, cooler, heater ...)

You can reuse:

- Sensors and codes,  to push to **Master**

- Pin Out needed to be activated/deactivated


.. note::

   **Master** is considered the center of decision

   **Nodes** will follow POWER OFF / POWER ON ordered by **Master**


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart/index
   components/index
   core/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

