#!/bin/bash

# Change directory to `~`.
cd ~ &&

# Update, upgrade, and install packages.
# Update and upgrade packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq update &&
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade &&
# Install packages.
yes | sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install build-essential cmake gfortran libatlas-base-dev libavcodec-dev libavformat-dev libgtk-3-dev libjasper-dev libjpeg8-dev libpng12-dev libswscale-dev libtiff5-dev libv4l-dev libx264-dev libxvidcore-dev pkg-config python-pip python2.7-dev python3-pip python3.5-dev &&

# Install `pip` packages.
sudo pip install virtualenv virtualenvwrapper &&

# Delete `pip` cache.
sudo rm -rf ~/.cache/pip &&

# Configure `.bashrc` for `virtualenv`.
sudo /bin/sh -c 'printf "\nexport WORKON_HOME=$HOME/.virtualenvs\nsource /usr/local/bin/virtualenvwrapper.sh" > ~/.bashrc' &&

# Restart `.bashrc`.
source ~/.bashrc &&

# Download and extract OpenCV source codes.
# Download OpenCV source codes.
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip &&
# Extract OpenCV source codes.
unzip opencv.zip &&

# Download and extract OpenCV add - ons.
# Download OpenCV add - ons.
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip &&
# Extract OpenCV add - ons.
unzip opencv_contrib.zip &&

# Make virtual environment for OpenCV compilation.
mkvirtualenv cv -p python3 &&

# Restart `.bashrc`.
source ~/.bashrc &&

# Activate virtual environment for OpenCV compilation.
workon cv &&

# Change directory to `~/opencv-3.1.0`.
cd ~/opencv-3.1.0/ &&

# Create `~/opencv-3.1.0/build` directory.
mkdir build &&

# Change directory to `~/opencv-3.1.0/build`.
cd build &&

# Configure OpenCV compilation.
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON .. &&

# Compile OpenCV.
make &&

# Install OpenCV.
sudo make install &&

# Restart `ldconfig`.
sudo ldconfig &&

# Deactivate virtual environment.
deactivate &&

# Copy OpenCV library into `/home/pedge/src/`.
ln -s /usr/local/lib/python3.5/site-packages/cv2.cpython-35m-x86_64-linux-gnu.so /home/pedge/src/cv2.so