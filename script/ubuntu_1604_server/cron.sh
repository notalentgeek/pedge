#!/bin/bash

# Change directory to `/home/pedge`.
cd /home/pedge &&

# Make launcher executable.
chmod +x /home/pedge/pedge/launcher/ubuntu_1604_server.sh &&

# Add Cron job.
echo -e "$(sudo crontab -u root -l)\n@reboot sh /home/pedge/pedge/launcher/ubuntu_1604_server.sh >/home/pedge/log_pedge_cron 2>&1" | sudo crontab -u root -