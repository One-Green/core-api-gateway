**************
Prepare master
**************

For **Master**, you can use any computer, but Raspberry Pi is very suitable for this use


.. note::

    To create Plant Keeper's Wifi access Point you need to add Wifi dongle.

    You can use any of Wifi dongle here:  https://www.elinux.org/RPi_USB_Wi-Fi_Adapters


Flash OS on Raspberry Pi
========================

1) Download Raspbian latest Image : https://www.raspberrypi.org/downloads/raspbian/

.. note::

    Linux familiar download **Raspbian Buster Lite**

    No Linux familiar download: **Raspbian Buster with desktop and recommended software**

2) Insert your SD Card (32Gi recommended) on computer used for flashing

3) Flash OS :

    Use Etcher https://www.balena.io/etcher/ , load image, select SD Card , run flash

4) Activate SSH:

    In flashed SD Card add in root an empty file **ssh**

.. warning::

    If you don't wan't use additional screen, keyboard, mouse: adding this file (**ssh**) will allow you to establish
    SSH communication trough local network, especially for **Raspbian Buster Lite** which does not come
    with a graphical interface


Prepare OS
==========

Connect to Rapbian trough SSH or start Terminal if you use desktop version

Upgrade
-------

.. code-block:: shell

    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo reboot


Install RasAP
-------------

Full documentation :  https://raspap.com/

RaspAP will create Wifi Access Point

Ensure Wifi dongle is plugged in USB

.. code-block:: shell

    curl -sL https://install.raspap.com | bash


Once installation completed, hardware restarted, you can access to

* **Web GUI for RaspAP**

    - IP address: 10.3.141.1

    - Username: admin

    - Password: secret

* **Wifi Access Point default configuration**

    - DHCP range: 10.3.141.50 to 10.3.141.255

    - SSID: raspi-webgui

    - Password: ChangeMe


You can connect on http://10.3.141.1 with user=admin and password=secret

1) Change RaspAP password http://10.3.141.1/index.php?page=auth_conf


2) Change Wifi Access Point configuration


.. figure:: ../images/raspap_ssid.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: flow


.. figure:: ../images/raspap_ssid_password.png
    :height: 100
    :width: 200
    :scale: 300
    :align: center
    :alt: flow


.. warning::

    Do not skip RaspAP SSID password configuration !

