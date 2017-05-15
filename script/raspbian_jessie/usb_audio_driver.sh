#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Create Alsa run command for system - wide USB audio driver.
sudo /bin/sh -c 'printf "\npcm.!default{\n    type hw card 1\n}\nctl.!default{\n    type hw card 1\n}" > /etc/asound.conf' &&

# Create Alsa run command for local USB audio driver.
sudo /bin/sh -c 'printf "\npcm.!default{\n    type hw card 1\n}\nctl.!default{\n    type hw card 1\n}" > /home/pi/.asoundrc' &&

# Configure Alsa for USB audio driver.
sudo sed -ie "s/defaults.ctl.card 0/defaults.ctl.card 1/g" /usr/share/alsa/alsa.conf &&
sudo sed -ie "s/defaults.pcm.card 0/defaults.pcm.card 1/g" /usr/share/alsa/alsa.conf &&
sudo sed -ie "s/defaults.pcm.device 0/defaults.pcm.device 1/g" /usr/share/alsa/alsa.conf &&
sudo sed -ie "s/defaults.pcm.subdevice 0/defaults.pcm.subdevice -1/g" /usr/share/alsa/alsa.conf &&
sudo sed -ie "s/defaults.pcm.subdevice 1/defaults.pcm.subdevice -1/g" /usr/share/alsa/alsa.conf