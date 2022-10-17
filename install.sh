#!/bin/bash

# remove previous installation
sudo rm -rf /usr/local/lib/spark
sudo rm -rf /usr/local/bin/spark

# install prerequisites
sudo dnf install -y python3 python3-pip
pip install InquirerPy rich

# install spark
rm -rf /tmp/spark
git clone "https://github.com/Kapsulon/spark.git" /tmp/spark/
cd /tmp/spark/
sudo chmod 777 *
sudo mv spark /usr/local/bin
cd ..
sudo mkdir /usr/local/lib/spark
sudo mv spark/* /usr/local/lib/spark/
