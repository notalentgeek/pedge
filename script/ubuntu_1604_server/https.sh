#!/bin/bash

# Change directory to `/home/pedge`.
cd /home/pedge &&

# Generate self - signed certificate for HTTPS.
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt