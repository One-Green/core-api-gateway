*****************
Play with Grafana
*****************

At this stage you don't need to setup ESP Node

We can use API to POST data to simulate sensors entry


Create dashboard: Sprinklers
============================


Plant-Keeper Master support multi Sprinkler, with unique **tag**

Each Sprinkler Node must send data to Api Gateway with a **tag**. **Tag** is created on the fly if not exist in database


Goto API Gateway : http://<raspberry_pi_IP>:8001/


.. figure:: ../images/api_gateway.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: api_gateway

Expand **sprinkler-valve** to send data trough web browser

.. figure:: ../images/api_gateway_sprinkler.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: api_gateway_sprinkler


.. note::

    Keep this page open, you will simulate Nodes


In another, page open Grafana

.. figure:: ../images/grafana_add_dashboard.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: grafana_add_dashboard


.. figure:: ../images/grafana_add_dashboard_2.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: grafana_add_dashboard
