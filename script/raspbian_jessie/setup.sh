#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&

# Make shell scripts to be executable.
sudo chmod +x /home/pi/pedge/script/raspbian_jessie/* &&

# Prevent screen saver.
sudo /home/pi/pedge/script/raspbian_jessie/prevent_screen_saver.sh &&

# Setup `cron`.
#sudo /home/pi/pedge/script/raspbian_jessie/cron.sh &&

# Setup `pyalsaaudio`.
sudo /home/pi/pedge/script/raspbian_jessie/pyalsaaudio.sh &&

# Setup LIRC.
sudo /home/pi/pedge/script/raspbian_jessie/lirc.sh &&

# Setup PICamera.
sudo /home/pi/pedge/script/raspbian_jessie/picamera.sh &&

# Setup PyAudio.
sudo /home/pi/pedge/script/raspbian_jessie/pyaudio.sh &&

# Setup USB audio driver.
sudo /home/pi/pedge/script/raspbian_jessie/usb_audio_driver.sh &&

# Install packages from `pip3`.
yes | sudo pip3 install -r /home/pi/pedge/requirement/raspbian_jessie.txt &&

# Delete `pip` cache.
sudo rm -rf /home/pi/.cache/pip &&

# Reboot.
reboot