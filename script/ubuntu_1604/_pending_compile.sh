#!/bin/bash

# Change directory to `~/pedge`
cd ~/pedge &&

# Delete previous compilation files and folders.
# Delete any `*.spec` files in `~/pedge/`.
rm ~/pedge/*.spec ||
# Delete `~/pedge/__pycache__`.
rm -r ~/pedge/__pycache__ ||
# Delete `~/pedge/build`.
rm -r ~/pedge/build ||
# Delete `~/pedge/dist`.
rm -r ~/pedge/dist ||
# Delete `~/pedge/log`.
rm -r ~/pedge/log ||
# Delete previous binary in `/usr/local/bin/pedge`.
sudo rm /usr/local/bin/pedge &&

# Compile.
pyinstaller \
    --paths="~/pedge/src" \
    --paths="~/pedge/src/cli" \
    --paths="~/pedge/src/config_and_database" \
    --paths="~/pedge/src/detection" \
    --paths="~/pedge/src/loose_lib" \
    --paths="~/pedge/src/manip" \
    --onefile ~/pedge/pedge.py &&

# Make `pedge` to be executable.
chmod +x ~/pedge/dist/pedge &&

# Copy `pedge` to `/usr/local/bin`.
sudo ln -s ~/pedge/dist/pedge /usr/local/bin/pedge