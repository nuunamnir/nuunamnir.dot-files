# nuunamnir's Arch Linux Installation and Configuration Files

## Table of Content
* [Table of Content](#table-of-content)
* [Screenshots](#screenshots)
* [Highlights](#highlights)
* [Dependencies](#dependencies)
* [Getting Started](#getting-started)

## Screenshots

## Highlights
* wallpaper dependent automated theme generation and application to "all" dependencies
* time and location dependent theme switcher for qtile
* periphery battery status widget (supports Bluetooth and Logitech Unified Receiver)

## Dependencies
* OS: [Arch Linux](https://www.archlinux.org/)
* WM: [Qtile](https://www.qtile.org/) + [picom](https://github.com/yshui/picom)
* Notifications: [dunst](https://github.com/dunst-project/dunst)
* Launcher: [rofi](https://github.com/davatorium/rofi)
* Shell: [zsh](https://www.zsh.org) + [starship](https://www.starship.rs/)
* Terminal: [kitty](https://sw.kovidgoyal.net/kitty/)
* Dotfiles: [nuunamnir.dot-files](https://github.com/nuunamnir/nuunamnir.dot-files)

## Getting Started
> No one size fits all and only change is permanent.

It needs to be understood that this repository is primarily meant for me, i.e., it is optimized to address my needs and solve my problems. It might not run on your machine (it might not even run on mine). However, it might contains some information that can be used as a starting point for others to solve their problems.

### Installation on a New Machine
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
1. Login as `root` and edit the sudoers file.
    ```
    EDITOR=vim visudo
    ```
1. Update the pacman keyring:
    ```
    pacman-key --init
    pacman-key --populate
    ```
1. Logout and login as a user; download and run the user installation script.
    ```
    wget https://raw.githubusercontent.com/nuunamnir/nuunamnir.dot-files/main/installation/user.sh
    ```
    The installation script performs the following actions:
    1. Installs these dot files.
    1. Installs yay.
    1. Installs rate-mirrors.
    1. Install qtile (including credentials).

    Adjust `user.sh` to change this behavior; then run:
    ```
    chmod +x user.sh
    ./user.sh
    ```

