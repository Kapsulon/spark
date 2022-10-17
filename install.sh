#!/bin/bash

sudo dnf install -y python3 python3-pip
pip install InquirerPy pyinstaller

rm -rf /tmp/spark
git clone "https://github.com/Kapsulon/spark.git" /tmp/spark/
cd /tmp/spark/
sudo chmod 777 *
mv spark /usr/local/bin
cd ..
mv spark/ /usr/local/lib
