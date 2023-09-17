#!/bin/bash

# Sets the time zone.
ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
hwclock --systohc

# Localizes the system.
sed -e "/en_US.UTF-8/s/^#*//g" -i /etc/locale.gen
sed -e "/de_DE.UTF-8/s/^#*//g" -i /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
echo "KEYMAP=de-latin1" >> /etc/vconsole.conf

# Sets the hostname.
echo "eridu" >> /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
echo "127.0.1.1 eridu.localdomain eridu" >> /etc/hosts

# Sets the root password.
echo root:password | chpasswd

# Creates a user.
useradd -m nuunamnir -p password -G wheel -s /usr/bin/zsh

# Installs the bootloader.
bootctl install
systemctl enable systemd-boot-update.service

systemctl enable dhcpcd.service