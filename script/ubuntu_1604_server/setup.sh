#!/bin/bash

# Change directory to `/home/pedge`.
cd /home/pedge &&

# Update packages for RethinkDB.
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list &&
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add - &&

# Update, upgrade, and install packages.
# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&
# Install packages.
yes | sudo apt-get install python3 python3-pip rethinkdb &&

# Make shell scripts to be executable.
sudo chmod +x /home/pedge/pedge/script/ubuntu_1604_server/* &&

# Setup `cron`.
sudo /home/pedge/pedge/script/ubuntu_1604_server/cron.sh &&

# Setup RethinkDB.
sudo /home/pedge/pedge/script/ubuntu_1604_server/rethinkdb.sh &&

# Setup self - signed certificate for HTTPS.
sudo /home/pedge/pedge/script/ubuntu_1604_server/https.sh &&

# Install packages from `pip3`.
# Fix locale error, [http://stackoverflow.com/questions/36394101/pip-install-locale-error-unsupported-locale-setting](http://stackoverflow.com/questions/36394101/pip-install-locale-error-unsupported-locale-setting).
export LC_ALL=C &&
yes | sudo pip3 install -r /home/pedge/pedge/requirement/ubuntu_1604_server.txt &&

# Delete `pip` cache.
sudo rm -rf /home/pedge/.cache/pip &&

# Reboot.
systemctl reboot -i