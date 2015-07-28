# rpi-music
Various things for using a Raspberry Pi for live music

## Bootstrap

Before the automated stuff, you'll need to do a bit of manual work to grab this repo.

### Image SD Card

First, use a standard raspbian image. Download the zip and image to an SD card. For me, with a brand new card, I had to format it to FAT first, then used Win32DiskImager on a windows machine to copy the image to the SD card. Put the card in the RPI and boot, with network.

This can also easily be done on linux from the command line as described at the [raspberrypi image installation instructions](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md)

	Download the latest raspbian (not NOOBS) image
	Run `df -h` to see what devices are mounted
	Insert SD
	Run `df -h` again to see the new one (typically /dev/sdd1)
	Unmount with `umount /dev/sdd1` (or wherever your SD was)
	Image with `dd bs=4M if=[raspbian.img] of=/dev/sdd` (note you don't include the 1, which is partition)

Again, note that with a completely fresh SD card, I had to format to FAT before it would let me write.



### Connect, update, install git, clone this repo

Figure out the IP address of the RPI (I went to my router's list of connected clients, and found the raspberry pi) and ssh to it. Username: pi, Password: raspberry

	$ sudo apt-get update
	$ sudo apt-get install git

Note, I also like having vim handy, so I also `sudo apt-get install vim`
	
You'll need proper credentials to clone, so copy private key (for github) up to RPI (in my case, I simply used ~/.ssh/id_rsa). Might as well create a ~/.ssh/config file with the following entry:

	host github.com
	  user git
	  IdentityFile ~/.ssh/id_rsa

This can be tested with a simple `ssh github.com`

Then clone this repo: `git clone git@github.com:chilkari/rpi-music.git`

### Finish raspbi config

`sudo raspi-config`

Expand the filesystem, change user password, internationalization - setup for your locale, and probably overclock. For audio, I tend to run on the 'high' setting 950.

### Easier ssh access from hosts

scp your public ssh key up to the pi: `scp [mykey] pi@[rpi ip address]:/home/pi/.ssh/authorized_keys`

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

### Wifi (optional)

Test that your wifi adapter is working with `sudo iwlist wlan0 scan` and find the SSID of your access point.

`sudo vim /etc/wpa_supplicant/wpa_supplicant.conf`

and add the following to the bottom:

	network={
            ssid="YOUR SSID"
            psk="WIFI PASSWORD"
        }

Wait, or do `sudo ifdown wlan0` then `sudo ifup wlan0`, or just `sudo reboot`

Verify by doing `ifconfig wlan0` and seeing an IP address.


### Setting Up a usable RPI Machine

Determine the type of machine you'd like {looper|sampler|organ} and set the MACHINE_TYPE variable in these files:

shutdown_monitor.sh
setup

If you're using a first generation RPI, edit the rpi-audio script and uncomment the RPI1=1 line.

The run setup.

Reboot - and you should be up and running.

