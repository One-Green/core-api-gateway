#!/usr/bin/env bash

# install Rasp AP (create dedicated Wifi access point)
curl -sL https://install.raspap.com | bash

# install docker-ce
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi

# install docker-compose
sudo apt python-pip
sudo pip install docker-compose

# Run Plant keeper
sudo docker-compose up
