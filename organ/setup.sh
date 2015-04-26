#!/bin/sh

# Add Autostatic PPA, and update, if necessary
if [ -f /etc/apt/sources.list.d/autostatic-audio-raspbian.list ];
then
    echo "autostatic PPA already here. Not adding...";
else
    wget -q -O - http://rpi.autostatic.com/autostatic.gpg.key | sudo apt-key add -
    sudo wget -q -O /etc/apt/sources.list.d/autostatic-audio-raspbian.list http://rpi.autostatic.com/autostatic-audio-raspbian.list
    sudo apt-get update
fi

# MidiMan 1x1 interface support
if [ -f /etc/udev/rules.d/99-midisport-firmware.rules ];
then
    echo "MidiMan 1x1 support already in place."
else
    sudo apt-get install midisport-firmware
    sudo cp midiman.conf /etc/udev/rules.d/99-midisport-firmware.rules
fi

# SETBFREE
if [ -f /usr/bin/setBfree ];
then
    echo "setBfree already installed."
else

    # Dependencies for setBfree
    sudo apt-get install libjack-dev libasound2 libasound2-dev libsndfile1 libsndfile1-dev libftgl-dev libglu1-mesa-dev ttf-bitstream-vera lv2-dev libzita-convolver-dev liblo-dev
    
    # Now, install from a deb file I have in S3. I'm not seeing this in normal
    # raspbian repos, but it seems to sort of be in the ubuntu launchpad for arm.
    # TODO - sort this out so I have the latest version...
    
    wget https://s3-us-west-2.amazonaws.com/chilkari-raspberry-pi-music/setbfree_0.7.5-1_armhf.debsudo dpkg -i setbfree_0.7.5-1_armhf.deb
    # Ensure we have deps:
    sudo apt-get install -f
    # Remove unneeded packages
    sudo apt-get autoremove
    # Remove the downloaded setbfree deb file:
    rm setbfree_0.7.5-1_armhf.deb
fi


# TODO - init.d script...

