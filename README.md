# rpi-music
Various things for using a Raspberry Pi for live music

## Bootstrap

Before the easy stuff, you'll need to do a bit of manual work to grab this repo.

### Image SD Card

First, use a standard raspbian image. Download the zip and image to an SD card. For me, with a brand new card, I had to format it to FAT first, then used Win32DiskImager on a windows machine to copy the image to the SD card. Put the card in the RPI and boot, with network.

### Connect, update, install git, clone this repo

Figure out the IP address of the RPI (I went to my router's list of connected clients, and found the raspberry pi) and ssh to it. Username: pi, Password: raspberry

	$ sudo apt-get update
	$ sudo apt-get install git
	
You'll need proper credentials to clone, so copy private key (for github) up to RPI (in my case, I simply used ~/.ssh/id_rsa). Might as well create a ~/.ssh/config file with the following entry:

	host github.com
	  user git
	  IdentityFile ~/.ssh/id_rsa

This can be test with a simple `ssh github.com`

Then clone this repo: `git clone git@github.com:chilkari/rpi-music.git`

### Static IP (optional)

You might want to give your RPI a static IP on your network for more reliable SSH connections.

http://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address

ifconfig 
-- grab Bcast and Mask from eth0

netstat -nr
-- grab Gateway (192.168.xxx) and Destination (192.168.1.0)

    sudo vim /etc/network/interfaces

Change 

    iface eth0 inet dhcp

to

    iface eth0 inet static
    address 192.168.1.132
    netmask 255.255.255.0   (Mask from ifconfig)
    network 192.168.1.0     (Destination from netstat)
    broadcast 192.168.1.255 (Bcast from ifconfig)
    gateway 192.168.1.1     (Gateway from netstat)
   

And reboot (sudo reboot)


