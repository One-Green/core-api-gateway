.. image:: https://github.com/One-Green/plant-keeper-master/workflows/BUILD/badge.svg
   :target: https://github.com/One-Green/plant-keeper-master/actions?query=workflow%3ABUILD

.. image:: https://img.shields.io/badge/Python-3.10.2-<COLOR>.svg
   :target: https://www.python.org

.. image:: https://readthedocs.org/projects/one-green/badge/?version=latest
    :target: https://one-green.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/CC-BY--SA%204.0-lightgrey
   :target: https://creativecommons.org/licenses/by-nc/4.0/

.. image:: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg
   :target: mailto:shanmugathas.vigneswaran@outlook.fr




Summary
=======

This project provides a complete framework for plant cultivation both indoors and outdoors.

Core
----

The framework is composed of a **Core** including functionalities such as:

- MQTT for data ingestion and callback

- API Gateway for configuration (written in Python/Django)

- Graphical interface to configure the components (Django admin interface)

- Interface for monitoring and alert management (Grafana)

- Controllers to ensure to send good signal to activated, deactivate valve, pump etc …

Nodes
-----

The second part of framework is Node ESP32 MicroPython Client class

Repository : https://github.com/One-Green/iot-edge-agent

We recommend to use GUI based flash tool : https://github.com/One-Green/iot-flash-config-tool/releases


Quick start
-----------

Install on kubernetes with Helm : https://artifacthub.io/packages/helm/one-green-core/one-green-core

More
====

Documentations : https://one-green.readthedocs.io/en/latest/?badge=latest
