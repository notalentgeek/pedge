#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Configure boot setup.
sudo sed -ie "/start_x=0/d" /boot/config.txt &&
sudo /bin/sh -c 'printf "\nstart_x=1\ngpu_mem=128" >> /boot/config.txt'