#!/bin/bash

# Change directory to `/home/pedge`.
cd /home/pedge &&

# Configure RethinkDB to start when operating system boot.
sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf &&
sudo sed -ie "s/# bind=127.0.0.1/bind=all/g" /etc/rethinkdb/instances.d/instance1.conf