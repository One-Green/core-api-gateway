WIP
===

- Tests
- Controller for Raspberry PI

Before start
============

You should have some basics knowledge :

- Python OO :
- Django Framework : https://www.djangoproject.com/
- RESTful tutorial : https://www.restapitutorial.com/
- Django Rest Framework : https://www.django-rest-framework.org/


Python and Django Based Plant controller
========================================

With this project you can automate plant growing ecosystem.

Use HTTP Rest API to save sensors values into database.


**Fully compatible with Raspberry PI**


How it work
===========

Sensor have ORM model (SQL table and relation representation in Python code with Django backend).

Action devices have also ORM model.

These ORM are used to save latest values such as : Enclosure temperature, water filling pump power status ...

There is special ORM model **plant_core.models.PlantSettings**, this one is used to save plant set point such as :

- Air Temperature
- Air Hygrometry
- Soil Hygrometry


1) Values inputs

- HTTP API

- Django ORM API


Binary controller & controller aggregation
------------------------------------------

Related class **core.controller.BaseController**

To take a device action based on sensor, a controller is needed.

BaseController require 3 arguments: type of controller, neutral point,
maximum delta, minimum delta.

- Type of controller must be string = 'CUT_IN' or 'CUT_OUT', in most case you should use 'CUT_OUT'
there is a video to explain : https://www.youtube.com/watch?v=VwMn-5NV5eM

- Neutral point must be float, this a set point value, system always try to fit this value

- maximum delta and minimum delta :
    - if kind 'CUT_OUT' maximum delta is needed: action device will be in "POWER=ON" status if
      [sensor value] is greater than / equal to  [set point (= neutral point)  + maximum delta]. In
      Other conditions device be in "POWER=OFF"
    - if kind 'CUT_IN' minimum delta is needed [WIP]

Related class **core.aggregator.BaseAggregator**

In common case, one controller handle one device.

In some case, we can fact with two or three controller acting on one device. The meaning : one device assume more than one function.
A Peltier Cooling cell can decrease temperature, decrease hygrometry.
Use BaseAggregator([temperature_controller, hygrometry_controller]) to get only one action to take for a device.
Have a look in **controller.tests.peltier_controller.py** to test Aggregator.


Installation
------------

1) Install Python 3.7.4 and Pipenv

Use shell script **install_python_3.7.4.sh** to install Python 3.7.4,
this script will also install Pipenv.

.. code-block:: shell

    sudo bash install_python_3.7.4.sh


2) Install project packages from Pipfile

.. code-block:: shell

    sudo pipenv install

3) Make database migrations and do migrate

Before running Django server you need to create migrations, and update database.
(plant_core.models ORM to SQL tables and relations)

.. code-block:: shell

    sudo pipenv run python manage.py makemigrations
    sudo pipenv run python manage.py migrate

4) Create an admin user

To configure plant temperature, hygrometry, chart temperature sensors etc ... you must create and admin

.. code-block:: shell

    sudo pipenv run python manage.py createsuperuser
    # fill input requested by command line interface

5) Runserver

Run server and open a web browser to:

- http://localhost:8000 -> display Swagger API

- http://localhost:8000/admin -> to login in admin interface


End to end test a controller
============================

Run server with:

.. code-block:: shell

    sudo pipenv run python manage.py runserver

Open web browser, login, and create PlantSettings entry , controller wil try to load these values.

Run Peltier controller

.. code-block:: shell

    cd controllers && pipenv run python peltier.py

- In web browser use Swagger

- Select "/enclosure/" POST method

- Click on "Try it out"

- Enter manually values

- Click on "Execute"