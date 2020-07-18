.. image:: docs/images/main_logo.png
   :width: 200
   :align: center

.. image:: https://img.shields.io/badge/Python-3.8.1-<COLOR>.svg
   :target: https://www.python.org

.. image:: https://readthedocs.org/projects/plant-keeper/badge/?version=latest
    :target: https://plant-keeper.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/shanisma/plant-keeper.svg?branch=master
   :target: https://travis-ci.org/shanisma/plant-keeper

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg
   :target: https://creativecommons.org/publicdomain/zero/1.0/deed.en

.. image:: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg
   :target: mailto:shanmugathas.vigneswaran@outlook.fr


Summary
=======

This project provides a complete framework for plant cultivation both indoors and outdoors.

Master
------

The framework is composed of a Master including functionalities such as:

- API Gateway for data digestion (written in Python/Django)

- Graphical interface to configure the components (Django admin interface – future is Angular webapp !)

- Interface for monitoring and alert management (Grafana)

- Controllers to ensure to send good signal to activated, deactivate valve, pump etc …

Nodes
-----

The second part of framework is Node ESP32 MicroPython Client class

Repository : https://github.com/shanisma/pk-node-client

Import client, select Node Type (sprinkler, water pump, cooler, heater …)

Reuse:

sensors + codes to push to Master
Pin Out needed to be activated/deactivated


.. image:: docs/images/grafana_1-min.png
   :width: 600
   :align: center


QuickStart : Docker way
=======================

Tested with this configuration

- Server board : Raspberry PI 3 B+

- Wifi dongle for creating Wifi Access Point: TP-Link TL-WN823N

- Docker + docker-compose installed


.. code-block:: shell

    git clone https://github.com/shanisma/plant-keeper.git
    cd plant-keeper
    docker-compose up -d

QuickStart: Install MicroK8s
============================

Install tiny Kubernetes cluster on you machine (Raspberry Pi compatible): https://microk8s.io/


.. code-block:: shell

    # install snap + add snap binaries in PATH
    sudo apt update
    sudo apt install snapd
    sudo echo "export PATH=\$PATH:/snap/bin" >> ~/.bashrc
    sudo source ~/.bashrc

    # Install MicroK8s + Helm
    sudo snap install microk8s --classic
    sudo sed -i '${s/$/ cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1/}' /boot/firmware/cmdline.txt
    sudo microk8s.enable dns dashboard storage ingress helm3
    sudo microk8s.stop
    sudo microk8s.start
    sudo microk8s.helm init --upgrade

    # Create Aliases
    echo "alias kubectl=\"sudo microk8s.kubectl\"" >> ~/.bashrc
    echo "alias k=\"sudo microk8s.kubectl\"" >> ~/.bashrc

    echo "alias helm=\"sudo microk8s.helm\"" >> ~/.bashrc
    echo "alias h=\"sudo microk8s.helm\"" >> ~/.bashrc
    source ~/.bashrc


QuickStart: Kubernetes
======================

Deploy Plant Keeper in Kubernetes

- Helm chart for Loki and Grafana

- Yaml files for TimeScaleDB , Plant-Keeper Api GateWay , Plant-Keeper Controllers

.. code-block:: shell

    # Raspbery Pi => suppose microk8s is used
    kubectl create namespace plant-keeper

    helm repo add stable https://kubernetes-charts.storage.googleapis.com
    helm repo add loki https://grafana.github.io/loki/charts
    helm repo update
    helm upgrade --install grafana stable/grafana -n plant-keeper \
        --set persistence.enabled=true \
        --set persistence.type=pvc \
        --set persistence.size=1Gi \
        --set storageClassName=microk8s-hostpath

    helm upgrade --install loki loki/loki  -n plant-keeper

    # Apply manifest from this repository
    kubectl apply -f kubernetes/ -n plant-keeper


More
====


Documentations : https://plant-keeper.readthedocs.io/en/latest/?badge=latest
