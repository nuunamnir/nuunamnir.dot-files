# nuunamnir's Arch Linux Installation and Configuration Files

## Table of Content
* [Table of Content](#table-of-content)
* [Screenshots](#screenshots)
* [Conventions](#conventions)

## Screenshots

## Getting Started
> No one size fits all and only change is permanent.

It needs to be understood that this repository is primarily meant for me, i.e., it is optimized to address my needs and solve my problems. It might not run on your machine (it might not even run on mine). However, it might contains some information that can be used as a starting point for others to solve their problems.

## Installation on a New Machine
1. Get the latest Arch Linux image from a trusted [source](https://archlinux.org/download/).
1. Boot into the live environment.
    * Set the correct keyboard layout:
        ```
        loadkeys de-latin1
        ```
    * Establish a connection to the internet.
        > ***TODO:*** Extend guide for wireless installation.
    * Ensure that the system clock is accurate.
1. Partition the disks using `gdisk`.
    * Set up a partition for the booloader with size 1 GiB.
    * Set up a partiton for swap depending on your memory and disk size.
    * Allocate at least 128 GiB of disk space for the root partition.
1. Format the partitions:
    ```
    mkfs.fat -F 32 /dev/sda1
    mkswap /dev/sda2
    mkfs.btrfs /dev/sda3
1. Mount the partitions:
    ```
    mount /dev/sda3 /mnt
    mount --mkdir /dev/sda1 /mnt/boot
    swapon /dev/sda2
    ```
1. Assign a label to the root parition.
    ```
    btrfs filesystem label /dev/sda3 "Arch Linux"
    ```
1. Install essential packages:
    ```
    pacstrap -K /mnt base linux linux-firmware
    ```
1. Generate an `fstab` file:
    ```
    genfstab -U /mnt >> /mnt/etc/fstab
    ```
1. Change root into the new system:
    ```
    arch-chroot /mnt
    ```
1. Download and run the installation script.
    ```
    wget https://raw.githubusercontent.com/nuunamnir/nuunamnir.dot-files/main/installation/base.sh
    ```
    The installation script performs the following actions:
    1. Sets the time zone.
    1. Localizes the system.
    1. Sets the hostname.
    1. Sets the root password.
    1. Installs essential packages.
    1. Creates a user.
    1. Installs the boot manager.

    Adjust `base.sh` to change this behavior; then run:
    ```
    chmod +x base.sh
    ./base.sh
    ```
1. Leave the root environment.
    ```
    exit
    ```
1. Unmount partitions and reboot.
    ```
    umount -R /mnt
    reboot
    ```

## Conventions
* Arch linux is installed
* numlock is active
    * install this by running `yay -S mkinitcpio-numlock`  
    * enable this by adding `numlock` to `HOOKS` in `/etc/mkinitcpio.conf`

