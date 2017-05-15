#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Update, upgrade, and install packages.
# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&
# Install packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install lirc liblircclient-dev &&

# Configure boot setup.
sudo /bin/sh -c 'printf "\ndtoverlay=lirc-rpi,gpio_in_pin=23,gpio_out_pin=22" >> /boot/config.txt' &&

# Configure GPIO for IR transceiver.
sudo /bin/sh -c 'printf ""\nlirc_dev\nlirc_rpi gpio_in_pin=23 gpio_out_pin=22"" >> /etc/modules' &&

# Create local LIRC run commands.
sudo /bin/sh -c 'printf "\nbegin\n    button = KEY_1\n    config = KEY_1\n    prog = pysoc\nend\nbegin\n    button = KEY_2\n    config = KEY_2\n    prog = pysoc\nend\nbegin\n    button = KEY_3\n    config = KEY_3\n    prog = pysoc\nend" > /home/pi/.lircrc' &&

# Create system - wide LIRC run commands.
sudo /bin/sh -c 'printf "\nbegin\n    button = KEY_1\n    config = KEY_1\n    prog = pysoc\nend\nbegin\n    button = KEY_2\n    config = KEY_2\n    prog = pysoc\nend\nbegin\n    button = KEY_3\n    config = KEY_3\n    prog = pysoc\nend" > /etc/lirc/lircrc' &&

# Re - create hardware configuration.
# Delete hardware configuration.
sudo rm /etc/lirc/hardware.conf &&
# Create hardware configuration.
sudo /bin/sh -c 'printf "\n########################################################\n# /etc/lirc/hardware.conf\n#\n# Arguments which will be used when launching lircd\nLIRCD_ARGS=\"--uinput\"\n\n# Do not start lircmd even if there seems to be a good config file\n# START_LIRCMD=false\n\n# Do not start irexec, even if a good config file seems to exist.\n# START_IREXEC=false\n\n# Try to load appropriate kernel modules\nLOAD_MODULES=true\n\n# Run \"lircd --driver=help\" for a list of supported drivers.\nDRIVER=\"default\"\n# usually /dev/lirc0 is the correct setting for systems using udev\nDEVICE=\"/dev/lirc0\"\nMODULES=\"lirc_rpi\"\n\n# Default configuration files for your hardware if any\nLIRCD_CONF=\"\"\nLIRCMD_CONF=\"\"\n########################################################" > /etc/lirc/hardware.conf' &&

# Re - create IR dictionary.
# Delete IR dictionary.
sudo rm /etc/lirc/lircd.conf &&
# Create IR dictionary.
sudo /bin/sh -c 'printf "\n# Please make this file available to others\n# by sending it to <lirc@bartelmus.de>\n#\n# this config file was automatically generated\n# using lirc-0.9.0-pre1(default) on Sat Jan  7 22:45:56 2017\n#\n# contributed by \n#\n# brand:                       /home/pi/lircd.conf\n# model no. of remote control: \n# devices being controlled by this remote:\n#\nbegin remote\n  name  pysoc\n  bits           13\n  flags RC5|CONST_LENGTH\n  eps            30\n  aeps          100\n  one           924   840\n  zero          924   840\n  plead         970\n  gap          113287\n  toggle_bit_mask 0x0\n      begin codes\n          KEY_1                    0x1001\n          KEY_2                    0x1002\n          KEY_3                    0x1003\n      end codes\nend remote" > /etc/lirc/lircd.conf' &&

# Re - start LIRC service.
# Stop LIRC service.
sudo /etc/init.d/lirc stop &&
# Start LIRC service.
sudo /etc/init.d/lirc start