#!/bin/bash

# Change directory to `~`.
cd ~ &&

# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&

# Make shell scripts to be executable.
sudo chmod +x ~/pedge/script/rasbian_jessie/* &&

# Setup `pyalsaaudio`.
sudo ~/pedge/script/ubuntu_1604_jessie/pyalsaaudio.sh &&

# Setup OpenCV.
sudo ~/pedge/script/ubuntu_1604_jessie/opencv.sh &&

# Setup PyAudio.
sudo ~/pedge/script/ubuntu_1604_jessie/pyaudio.sh &&

# Install packages from `pip3`.
yes | sudo pip3 install -r ~/pedge/requirement/ubuntu_1604_jessie.txt &&

# Delete `pip` cache.
sudo rm -rf ~/.cache/pip &&

# Compile `pedge`.
# sudo ~/pedge/script/ubuntu_1604_jessie/pedge.sh