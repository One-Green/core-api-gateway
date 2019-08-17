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
                        libffi-dev \
                        ca-certificates

git clone git://git.openssl.org/openssl.git
cd openssl
./config # --prefix=/usr use this for OrangePi
make
make test
sudo make install
cd ..
sudo ldconfig


wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
tar xf Python-3.7.4.tar.xz
cd Python-3.7.4
sudo ./configure #  --enable-optimizations arm compilation in error , use gcc
sudo make -j 4
sudo make install
sudo cd .. && rm -rv Python-3.7.4
sudo pip3.7 install pipenv