#!/bin/bash

# Change directory to `~`.
cd ~ &&

# Install packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install python-pip python3-pip

# Download and extract PortAudio Stable version 19 source codes.
# Download PortAudio Stable version 19 source codes.
wget http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz -P ~ &&
# Extract PortAudio Stable version 19 source codes.
tar xf ~/pa_stable_v19_20140130.tgz -C ~ &&

# Change directory to `~/portaudio.
cd ~/portaudio &&

# Configure PortAudio Stable version 19.
./configure &&

# Compile PortAudio Stable version 19.
make &&

# Install PortAudio Stable version 19.
sudo make install &&

# Change directory to `~`.
cd ~ &&

# Configure `~/.bashrc` for PortAudio Stable version 19.
sudo /bin/sh -c 'printf "\nLD_LIBRARY_PATH=\"/usr/local/lib\"\nexport LD_LIBRARY_PATH\nLD_RUN_PATH=\"/usr/local/lib\"\nexport LD_RUN_PATH\nPATH=$PATH:/usr/local/lib/\nexport PATH" >> ~/.bashrc' &&

# Install PyAudio for Python 2.x.
sudo pip install pyaudio &&

# Install PyAudio for Python 3.x.
sudo pip3 install pyaudio &&

# Delete `pip` cache.
sudo rm -rf ~/.cache/pip