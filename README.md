# rpi-music
Various things for using a Raspberry Pi for live music

## Bootstrap

Before the easy stuff, you'll need to do a bit of manual work to grab this repo.

First, use a standard raspbian image. Download the zip and image to an SD card. For me, with a brand new card, I had to format it to FAT first, then used Win32DiskImager on a windows machine to copy the image to the SD card. Put the card in the RPI and boot, with network.

Figure out the IP address of the RPI (I went to my router's list of connected clients, and found the raspberry pi) and ssh to it. Username: pi, Password: raspberry

	$ sudo apt-get update
	$ sudo apt-get install git
	
You'll need proper credentials to clone, so copy private key (for github) up to RPI (in my case, I simply used ~/.ssh/id_rsa). Might as well create a ~/.ssh/config file with the following entry:

	host github.com
	  user git
	  IdentityFile ~/.ssh/id_rsa

This can be test with a simple `ssh github.com`

Then clone this repo: `git clone git@github.com:chilkari/rpi-music.git`

