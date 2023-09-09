# Arch Linux Installation

## Prerequisits

The scripts assume that you have:

1. set the console keyboard layout
```
loadkeys de-latin1
```

2. established an internet connection

3. updated the system clock
```
timedatectl set-ntp true
```

4. partitioned the disks and mounted the root volume to /mnt

5. installed essential packages
```
pacstrap /mnt base linux linux-firmware vim git
```

6. generated the fstab file
```
genfstab -U /mnt >> /mnt/etc/fstab
```

7. chrooted into the new system
```
arch-chroot /mnt
```

## Usage

Download this repository with
```
git clone https://github.com/nuunamnir.dot-files.git
```

Switch into the installation directory, edit the required scripts according to your hardware and software needs, and then execute it (replace script with the respective script name):
```
chmod +x script.sh
./script.sh
```

### Enable Automated Time Synchronization
As root, run the following commands:
```
systemctl enable systemd-timesyncd.service
systemctl start systemd-timesyncd.service
```

## Acknowledgements

The initial version of this script is heavily inspired by [eflinux](https://gitlab.com/eflinux/arch-basic).
