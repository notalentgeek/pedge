#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Update, upgrade, and install packages.
# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&
# Install packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install gcc libasound2-dev python3-dev

# Download `pyalsaaudio` source codes.
git clone https://github.com/larsimmisch/pyalsaaudio.git

# Change directory to `/home/pi/pyalsaaudio`.
cd /home/pi/pyalsaaudio

# Compile `pyalsaaudio` source codes.
python3 setup.py build

# Install `pyalsaaudio` source codes.
python3 setup.py install