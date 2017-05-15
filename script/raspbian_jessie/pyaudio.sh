#!/bin/bash

# Change directory tos `/home/pi`.
cd /home/pi &&

# Update, upgrade, and install packages.
# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&
# Install packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install python-dev python-pip python3-dev python3-pip &&

# Download and extract PortAudio Stable version 19 source codes.
# Download PortAudio Stable version 19 source codes.
wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz -P /home/pi &&
# Extract PortAudio Stable version 19 source codes.
tar xf /home/pi/pa_stable_v19_20140130.tgz -C /home/pi &&

# Change directory to `/home/pi/portaudio.
cd /home/pi/portaudio &&

# Configure PortAudio Stable version 19.
./configure &&

# Compile PortAudio Stable version 19.
make &&

# Install PortAudio Stable version 19.
sudo make install &&

# Change directory to `/home/pi`.
cd /home/pi &&

# Configure `/home/pi/.bashrc` for PortAudio Stable version 19.
sudo /bin/sh -c 'printf "\nLD_LIBRARY_PATH=\"/usr/local/lib\"\nexport LD_LIBRARY_PATH\nLD_RUN_PATH=\"/usr/local/lib\"\nexport LD_RUN_PATH\nPATH=$PATH:/usr/local/lib/\nexport PATH" >> /home/pi/.bashrc' &&

# Install PyAudio package from `pip`.
sudo pip install pyaudio &&

# Install PyAudio package from `pip3`.
sudo pip3 install pyaudio &&

# Delete `pip` cache.
sudo rm -rf /home/pi/.cache/pip