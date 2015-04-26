#!/bin/sh

# MidiMan 1x1 interface support
sudo apt-get install midisport-firmware
sudo cp midiman.conf /etc/udev/rules.d/99-midisport-firmware.rules

# Dependencies for setBfree compilation
sudo apt-get install libjack-dev libasound2 libasound2-dev libsndfile1 libsndfile1-dev libftgl-dev libglu1-mesa-dev ttf-bitstream-vera lv2-dev libzita-convolver-dev liblo-dev

if [ -d ../setBfree ];
then
   echo "setBfree exists... not cloning";
else
   cd ..;
   git clone git@github.com:pantherb/setBfree.git;
   cd setBfree;
   make OPTIMIZATIONS="-ffast-math -O3";
   sudo make install;
fi
