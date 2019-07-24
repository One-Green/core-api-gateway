#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y build-essential \
                        tk-dev \
                        libncurses5-dev \
                        libncursesw5-dev \
                        libreadline6-dev \
                        libdb5.3-dev \
                        libgdbm-dev \
                        libsqlite3-dev \
                        libssl-dev \
                        libbz2-dev \
                        libexpat1-dev \
                        liblzma-dev \
                        zlib1g-dev \
                        libffi-dev
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
sudo tar zxf Python-3.7.4.tgz
cd Python-3.7.4
sudo ./configure
sudo make -j 4
sudo make altinstall
sudo cd .. && rm -rv Python-3.7.4
sudo pip3.7 install pipenv