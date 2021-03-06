#!/bin/bash

ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
hwclock --systohc

sed -e "/en_US.UTF-8/s/^#*//g" -i /etc/locale.gen
sed -e "/de_DE.UTF-8/s/^#*//g" -i /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
echo "KEYMAP=de-latin1" >> /etc/vconsole.conf

# replace nippuur with desired hostname
echo "nippuur" >> /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
echo "127.0.1.1 nippuur.localdomain nippuur" >> /etc/hosts

# replace password with desired root password
echo root:password | chpasswd

pacman -S reflector
reflector -c Germany -a 6 --sort rate --save /etc/pacman.d/mirrorlist

pacman -S btrfs-progs zsh sudo base-devel iwd dhcpcd openssh

mkdir repositories
cd repositories
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ../..

pacman -S bluez bluez-utils
pacman -S intel-ucode
pacman -S nvidia nvidia-utils nvidia-settings

yay -S zramd
systemctl enable zramd

# additional firmware (mainly to surpress warnings)
yay -S upd72020x-fw

systemctl enable idw.service
systemctl enable dhcpcd.service
systemctl enable bluetooth.service

# replace nuunamnir and password with desired user name and password
# !!! adds user to the wheel group !!!
useradd -m nuunamnir -p password -G wheel -s /usr/bin/zsh

# uncomment the wheel rule
visudo
