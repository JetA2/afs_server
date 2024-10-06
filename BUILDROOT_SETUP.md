## Buildroot

Buildroot base:
https://github.com/sirsipe/buildroot-externals/tree/main (rpi-wifi, floppy_sound)

make BR2_EXTERNAL=../buildroot-externals:/mnt/Development/Source/Projects/AmigaFloppySelector/floppy_sound menuconfig

Hostname:
floppy

Root password:
root

Extra target packages:

python3
│ -> Target packages
│ -> Interpreter languages and scripting

python-sh
python-alsaaudio
│ -> Target packages  
│ -> Interpreter languages and scripting
│ -> python3 (BR2_PACKAGE_PYTHON3 [=y])
│ -> External python modules

libgpiod
│ -> Target packages
│ -> Libraries
│ -> Hardware handling

ntp (sntp, ntpd)
│ -> Target packages
│ -> Networking applications

raspi-gpio
│ -> Target packages  
│ -> Hardware handling

alsa-utils (all)
│ -> Target packages  
│ -> Audio and video applications

# config.txt

start_file=start.elf
fixup_file=fixup.dat
kernel=zImage
boot_delay=0
avoid_safe_mode=1
disable_splash=1
dtoverlay=dwc2
dtoverlay=audremap,pins_18_19

# cmdline.txt

root=/dev/mmcblk0p2 rootwait quiet console=tty1

**_ After first boot _**

# Install the AFS server

mkdir /root/afs
Copy the "afs_server" directory into the "afs" directory
Copy the floppy motor step sound file to the "afs" directory

# Partition the rest of the SD card

fdisk -l (List current partitions)
fdisk /dev/mmcblk0 (Substitute actual device)
Enter 'n' for new partition
Enter 'p' for primary partition
Enter next available partition number
Press 'Enter' for default partition start
Press 'Enter' to use all remaining space
Enter 'w' to save changes and exit

Reboot

mke2fs /dev/mmcblk0p3 (Substitute actual partition)

# Mount the storage partition

mkdir /mnt/storage
mount /dev/mmcblk0p3 /mnt/storage

# Create USB device image

dd bs=1M if=/dev/zero of=/mnt/storage/usb_device.bin count=16384 (16 GB image)
mkdosfs /mnt/storage/usb_device.bin -F 32 -I

# Mount the USB device image

mkdir /mnt/usb_device
mount /mnt/storage/usb_device.bin /mnt/usb_device -o users,umask=000

# Create the USB device file tree

mkdir /mnt/usb_device/FF
Copy the FF.CFG file to /mnt/usb_device/FF

# Update /etc/fstab

/dev/mmcblk0p3 /mnt/storage ext2 defaults 0 0
/mnt/storage/usb_device.bin /mnt/usb_device vfat users,umask=000 0 0

# Enable dwc2 and sound at boot

Update /etc/inittab:
After "::sysinit:/sbin/modprobe brcmfmac", add
::sysinit:/sbin/modprobe dwc2
::sysinit:/sbin/modprobe snd_bcm2835

# Start AFS server at boot

Update /etc/inittab:
After "::sysinit:/etc/init.d/rcS", add
::sysinit:/root/afs/start.sh

**_ Reboot _**
