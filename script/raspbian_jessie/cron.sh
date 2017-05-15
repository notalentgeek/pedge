#!/bin/bash

# Change directory to `/home/pi`.
cd /home/pi &&

# Make launcher executable.
chmod +x /home/pi/pedge/launcher/raspbian_jessie.sh &&

# Add Cron job.
echo -e "$(sudo crontab -u root -l)\n@reboot sh /home/pi/pedge/launcher/raspbian_jessie.sh >/home/pi/log_pedge_cron 2>&1" | sudo crontab -u root -