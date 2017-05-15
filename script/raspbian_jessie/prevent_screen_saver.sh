#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Configure `/etc/kbd/config`.
sudo sed -ie "s/BLANK_TIME=30/BLANK_TIME=0/g" /etc/kbd/config &&
sudo sed -ie "s/POWERDOWN_TIME=30/POWERDOWN_TIME=0/g" /etc/kbd/config &&

# Configure LightDM.
sudo sed -ie "s/#xserver-command=X/xserver-command=X -s 0 -dpms/g" /etc/lightdm/lightdm.conf &&

# Configure LXSession in `/etc/xdg/lxsession/LXDE-pi/autostart`.
sudo /bin/sh -c 'printf "\n@xset s noblank\n@xset s off\n@xset -dpms" >> /etc/xdg/lxsession/LXDE-pi/autostart' &&

# Configure LXSession in `/etc/xdg/lxsession/LXDE/autostart`.
sudo /bin/sh -c 'printf "\n@xset s noblank\n@xset s off\n@xset -dpms" >> /etc/xdg/lxsession/LXDE/autostart'