#!/bin/bash

# remove previous installation
sudo rm -rf /usr/local/lib/spark
sudo rm -rf /usr/local/bin/spark

# install prerequisites
if [ -f /etc/arch-release ]
then
    sudo pacman -S python python-pip docker --noconfirm
elif [ -f /etc/fedora-release ]
then
    sudo dnf install -y python3 python3-pip docker
fi

# install python dependencies
pip install InquirerPy rich requests

# build epitest daemon
sudo docker build -t epitest-server .

# init epitest daemon
./epitest-daemon

# install spark
sudo rm -rf /tmp/spark
git clone "https://github.com/Kapsulon/spark.git" /tmp/spark/
cd /tmp/spark/
sudo chmod 777 *
sudo mv spark /usr/local/bin
cd ..
sudo mkdir /usr/local/lib/spark
sudo mv spark/* /usr/local/lib/spark/
