WIP
===

- Tests
- Controller for Raspberry PI


Python and Django Based Plant controller
========================================

With this project you can automate plant growing ecosystem.

Use HTTP Rest API to save sensors values into database.

**Fully compatible with Raspberry PI**

Installation
============

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