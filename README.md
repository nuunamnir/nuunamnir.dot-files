# nuunamnir dot files

This is the collection of scripts and configuration files to set up my working environment. I tried to make them as reusable and automated as possile, but eventually my working environment is tailored towards my specific needs and idiosyncracies, so I expect that you need to tinker and adapt them to be useful for you.

## Table of Content

* [Table of Content]()
* [Screenshots]()
* [Color Scheme]()
* [OS Installation]()
   * [Arch Linux]()
      * [Installation Medium]()
      * [Skeleton System]()
      * [Setting Up DNS]()
      * [Install AUR Helper `yay`]()
      * [Setting Up SSH Access to the Local Machine]()
      * [Install Desktop Environment]()
* [Display Calibration]()

## Screenshots

## Color Scheme

The color scheme is designed to exploit the correlation lightness and colorfulness with perceptual saliency, allowing to assign certain meanings to the hue. More information of how these colors were selected can be found [here](https://www.github.com/nuunamnir/nuunamnir.color-scheme).

| <br>Name        | light<br>sRGB String | light<br>sRGB Numeric | light<br>Patch | dark<br>Patch | dark<br>sRGB Numeric |  dark<br>sRGB String |
| --------------- | -------------------- | --------------------- | -------------- | ------------- | -------------------- | -------------------- |
| cursor          | `#282828` | `(0.157, 0.157, 0.157)` | ![#282828](assets/282828.png) | ![#e5e5e5](assets/e5e5e5.png) | `(0.157, 0.157, 0.157)` | `#e5e5e5` |
| grey            | `#909090` | `(0.565, 0.565, 0.565)` | ![#909090](assets/909090.png) | ![#909090](assets/909090.png) | `(0.565, 0.565, 0.565)` | `#909090` |
| background      | `#e5e5e5` | `(0.898, 0.898, 0.898)` | ![#e5e5e5](assets/e5e5e5.png) | ![#282828](assets/282828.png) | `(0.898, 0.898, 0.898)` | `#282828` |
| foreground      | `#4d4d4d` | `(0.302, 0.302, 0.302)` | ![#4d4d4d](assets/4d4d4d.png) | ![#cbcbcb](assets/cbcbcb.png) | `(0.302, 0.302, 0.302)` | `#cbcbcb` |
| pastel_yellow   | `#69442d` | `(0.412, 0.267, 0.176)` | ![#69442d](assets/69442d.png) | ![#e4ba8b](assets/e4ba8b.png) | `(0.412, 0.267, 0.176)` | `#e4ba8b` |
| yellow          | `#7c3800` | `(0.486, 0.220, 0.000)` | ![#7c3800](assets/7c3800.png) | ![#ffb04c](assets/ffb04c.png) | `(0.486, 0.220, 0.000)` | `#ffb04c` |
| effect_light    | `#664900` | `(0.400, 0.286, 0.000)` | ![#664900](assets/664900.png) | ![#f0c532](assets/f0c532.png) | `(0.400, 0.286, 0.000)` | `#f0c532` |
| effect_light_muted | `#5c4c2e` | `(0.361, 0.298, 0.180)` | ![#5c4c2e](assets/5c4c2e.png) | ![#dec887](assets/dec887.png) | `(0.361, 0.298, 0.180)` | `#dec887` |
| effect_dark     | `#f0c532` | `(0.941, 0.773, 0.196)` | ![#f0c532](assets/f0c532.png) | ![#664900](assets/664900.png) | `(0.941, 0.773, 0.196)` | `#664900` |
| effect_dark_muted | `#dec887` | `(0.871, 0.784, 0.529)` | ![#dec887](assets/dec887.png) | ![#5c4c2e](assets/5c4c2e.png) | `(0.871, 0.784, 0.529)` | `#5c4c2e` |
| positive        | `#455600` | `(0.271, 0.337, 0.000)` | ![#455600](assets/455600.png) | ![#c0d958](assets/c0d958.png) | `(0.271, 0.337, 0.000)` | `#c0d958` |
| green           | `#455600` | `(0.271, 0.337, 0.000)` | ![#455600](assets/455600.png) | ![#c0d958](assets/c0d958.png) | `(0.271, 0.337, 0.000)` | `#c0d958` |
| pastel_green    | `#4a522f` | `(0.290, 0.322, 0.184)` | ![#4a522f](assets/4a522f.png) | ![#c6d397](assets/c6d397.png) | `(0.290, 0.322, 0.184)` | `#c6d397` |
| cyan            | `#00644e` | `(0.000, 0.392, 0.306)` | ![#00644e](assets/00644e.png) | ![#2de9cc](assets/2de9cc.png) | `(0.000, 0.392, 0.306)` | `#2de9cc` |
| pastel_cyan     | `#3e5c52` | `(0.243, 0.361, 0.322)` | ![#3e5c52](assets/3e5c52.png) | ![#9dd9cb](assets/9dd9cb.png) | `(0.243, 0.361, 0.322)` | `#9dd9cb` |
| effect_complement_dark_muted | `#9cd7e2` | `(0.612, 0.843, 0.886)` | ![#9cd7e2](assets/9cd7e2.png) | ![#425c66](assets/425c66.png) | `(0.612, 0.843, 0.886)` | `#425c66` |
| effect_complement_dark | `#00e4ff` | `(0.000, 0.894, 1.000)` | ![#00e4ff](assets/00e4ff.png) | ![#006179](assets/006179.png) | `(0.000, 0.894, 1.000)` | `#006179` |
| effect_complement_light_muted | `#425c66` | `(0.259, 0.361, 0.400)` | ![#425c66](assets/425c66.png) | ![#9cd7e2](assets/9cd7e2.png) | `(0.259, 0.361, 0.400)` | `#9cd7e2` |
| neutral         | `#006179` | `(0.000, 0.380, 0.475)` | ![#006179](assets/006179.png) | ![#5bd9ff](assets/5bd9ff.png) | `(0.000, 0.380, 0.475)` | `#5bd9ff` |
| effect_complement_light | `#006179` | `(0.000, 0.380, 0.475)` | ![#006179](assets/006179.png) | ![#00e4ff](assets/00e4ff.png) | `(0.000, 0.380, 0.475)` | `#00e4ff` |
| pastel_blue     | `#415670` | `(0.255, 0.337, 0.439)` | ![#415670](assets/415670.png) | ![#a3cfe0](assets/a3cfe0.png) | `(0.255, 0.337, 0.439)` | `#a3cfe0` |
| blue            | `#005797` | `(0.000, 0.341, 0.592)` | ![#005797](assets/005797.png) | ![#5bd9ff](assets/5bd9ff.png) | `(0.000, 0.341, 0.592)` | `#5bd9ff` |
| pastel_magenta  | `#51466e` | `(0.318, 0.275, 0.431)` | ![#51466e](assets/51466e.png) | ![#ccbfdf](assets/ccbfdf.png) | `(0.318, 0.275, 0.431)` | `#ccbfdf` |
| magenta         | `#54369c` | `(0.329, 0.212, 0.612)` | ![#54369c](assets/54369c.png) | ![#d4b6ff](assets/d4b6ff.png) | `(0.329, 0.212, 0.612)` | `#d4b6ff` |
| pastel_red      | `#6b3e4d` | `(0.420, 0.243, 0.302)` | ![#6b3e4d](assets/6b3e4d.png) | ![#e1b2c5](assets/e1b2c5.png) | `(0.420, 0.243, 0.302)` | `#e1b2c5` |
| negative        | `#83254c` | `(0.514, 0.145, 0.298)` | ![#83254c](assets/83254c.png) | ![#ff9fca](assets/ff9fca.png) | `(0.514, 0.145, 0.298)` | `#ff9fca` |
| red             | `#83254c` | `(0.514, 0.145, 0.298)` | ![#83254c](assets/83254c.png) | ![#ff9fca](assets/ff9fca.png) | `(0.514, 0.145, 0.298)` | `#ff9fca` |

## OS Installation

### Arch Linux

#### Installation Medium

From an exisiting Arch Linux installation, you can create a bootable USB drive following these steps:
1. Install dependencies.
   ```bash
   sudo pacman -S wipe gptfdisk dosfstools
   ```
1. Wipe a USB drive using `wipe`. Warning: This will erase all data on the drive.
   ```bash
   sudo wipe /dev/sdX
   ```
   Replace `/dev/sdX` with your USB drive identifier.
2. Create a primary partition on the USB drive using `gdisk` and format the partition to FAT32.
    ```bash
    sudo gdisk /dev/sdX
    ```
    - Create a new partition with `n`, set the type to `EF02` (boot partition).
    - Write the changes with `w`.
    ```bash
    sudo mkfs.fat -F 32 /dev/sdX1
    ```
3. Mount the USB drive and extract the Arch Linux iso file to the mounted drive.
   ```bash
   sudo mount /dev/sdX1 /mnt
   sudo bsdtar -xf archlinux-YYYY.MM.DD-x86_64.iso -C /mnt
   ```
   Replace `YYYY.MM.DD` with the date of the Arch Linux release.
4. Unmount the USB drive.
   ```bash
   sudo umount /mnt
   ```

#### Skeleton System

Boot into the Arch Linux installation medium and follow these steps to install a skeleton system:
1. Set the keyboard layout.
   ```bash
   loadkeys de-latin1
   ```
2. Wipe the disk ussing `dd`. Warning: This will erase all data on the disk.
   ```bash
   dd if=/dev/urandom  of=/dev/nvme0nX bs=512 status=progress
   ```
   Replace `/dev/nvme0nX` with your disk identifier.
3. Create a new partition table using `gdisk`.
   ```bash
   gdisk /dev/nvme0nX
   ```
   - Create a new partition with `n`, set the type to `EF02` (boot partition, >2GiB).
   - Create a new partition with `n`, set the type to `8200` (Linux swap, >16GiB).
   - Create a new partition with `n`, set the type to `8300` (Linux filesystem).
   - Write the changes with `w`.
4. Format the partitions.
   ```bash
   mkfs.fat -F 32 /dev/nvme0nXp1
   mkswap /dev/nvme0nXp2
   swapon /dev/nvme0nXp2
   cryptsetup luksFormat /dev/nvme0nXp3
   cryptsetup open /dev/nvme0nXp3 cryptroot
   mkfs.btrfs -L root /dev/mapper/cryptroot
   mount /dev/mapper/cryptroot /mnt
   btrfs subvolume create /mnt/@
   btrfs subvolume create /mnt/@home
   umount /mnt
   ```
5. Mount the subvolumes.
   ```bash
   mount -o noatime,compress=zstd,space_cache=v2,ssd,discard=async,subvol=@ /mnt
   mkdir -p /mnt/{boot,home}
   mount -o noatime,compress=zstd,space_cache=v2,ssd,discard=async,subvol=@home /mnt/home
   mount /dev/nvme0nXp1 /mnt/boot
   ```
6. Install the base system (if you have an AMD cpu, adjust the ucode accordingly).
   ```bash
   pacstrap -K /mnt base base-devel linux linux-firmware btrfs-progs intel-ucode iwd dhcpcd openssh bluez bluez-utils pacman-contrib vim git
   ```
7. Generate the fstab file.
   ```bash
   genfstab -U /mnt >> /mnt/etc/fstab
   ```
8. Change root into the new system.
   ```bash
   arch-chroot /mnt
   ```
9. Set the timezone.
   ```bash
   ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
   timedatectl set-ntp true
   hwclock --systohc
   ```
10. Set the locale.
    ```bash
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
    echo "de_DE.UTF-8 UTF-8" >> /etc/locale.gen
    locale-gen
    echo "LANG=en_US.UTF-8" > /etc/locale.conf
    echo "KEYMAP=us" > /etc/vconsole.conf
    echo "XKBLAYOUT=us" >> /etc/vconsole.conf
    echo "XKBMODEL=us-intl" >> /etc/vconsole.conf
    echo "FONT=LatGrkCyr-12x22" >> /etc/vconsole.conf
    ```
11. Set the hostname.
    ```bash
    echo "arch" > /etc/hostname
    echo "127.0.0.1 localhost" > /etc/hosts
    echo "::1       localhost" >> /etc/hosts
    echo "127.0.1.1 arch.localdomain arch" >> /etc/hosts
    ``` 
12. Set the root password.
    ```bash
    passwd
    ```
13. Install the bootloader.
    ```bash
    bootctl --path=/boot install
    echo "default arch" > /boot/loader/loader.conf
    echo "timeout 0" >> /boot/loader/loader.conf
    ```
14. Initialize pacman keyring and install the necessary packages.
    ```bash
    pacman-key --init
    pacman-key --populate
    ```
15. Enable the necessary services.
    ```bash
    systemctl enable systemd-boot-update.service
    systemctl enable systemd-timesyncd.service
    systemctl enable systemd-resolved.service
    systemctl enable iwd.service
    systemctl enable dhcpcd.service
    systemctl enable bluetooth.service
    ```
16. Create a user account and set its password. Replace <USERNAME> with your desired username.
    ```bash
    useradd -m -G wheel -s /bin/bash <USERNAME>
    passwd <username>
    ```
17. Configure sudo for the user.
    ```bash
    sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /etc/sudoers
    ```
18. Add required modules (`btrfs`) and hooks (`encrypt` before filesystem) and regenerate the initramfs.
    ```bash
    mkinitcpio -P
    ```
19. Create bootloader entry.
    ```bash
    blkid > /boot/loader/entries/arch.conf
    echo "title Arch Linux" >> /boot/loader/entries/arch.conf
    echo "linux /vmlinuz-linux" >> /boot/loader/entries/arch.conf
    echo "initrd /intel-ucode.img" >> /boot/loader/entries/arch.conf
    echo "initrd /initramfs-linux.img" >> /boot/loader/entries/arch.conf
    echo "options cryptdevice=UUID=<UUID of /dev/nvme0nXp3>:root root=UUID=<UUID of /dev/mapper/cryptroot> rootflags=subvol=@" >> /boot/loader/entries/arch.conf
    ```
    Replace `<UUID of /dev/nvme0nXp3>` and `<UUID of /dev/mapper/cryptroot>` with the actual UUIDs of the partitions and delete the output of `blkid` in the file.
20. Exit the chroot environment and unmount the partitions.
    ```bash
    exit
    umount -R /mnt
    swapoff -a
    ```
21. Reboot the system.
    ```bash
    reboot
    ```

#### Setting Up DNS

After rebooting into the new system, set up DNS to resolve domain names:
1. Update `/etc/systemd/resolved.conf` to use a public DNS server.
   ```bash
   sudo vim /etc/systemd/resolved.conf
   ```
   A sample configuration might look like this:
   ```ini
   [Resolve]
   DNS=9.9.9.9#quad9.net 
   FallbackDNS=208.67.222.222#opendns.com 208.67.220.220#opendns.com
   Domains=~.
   DNSSEC=no
   MulticastDNS=yes
   LMNR=no
   ```

#### Install AUR Helper `yay`

After rebooting into the new system and establishing an internet connection, install `yay` to manage AUR packages:
1. Clone the `yay` repository.
   ```bash
   cd /tmp
   git clone https://aur.archlinux.org/yay.git
   cd yay
   ```
2. Build and install `yay`.
   ```bash
   makepkg -si
   ```
3. Install `rate-mirrors` to optimize package downloads.
   ```bash
   sudo yay -S rate-mirrors-bin
   ```
   Add the following to your `~/.bashrc` to use `rate-mirrors`:
   ```bash
    alias yay-drop-caches='sudo paccache -rk3; yay -Sc --aur --noconfirm'
    alias yay-update-all='export TMPFILE="$(mktemp)"; \
      sudo true; \
      rate-mirrors --entry-country=DE --save=$TMPFILE arch --max-delay=21600 \
      && sudo mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist-backup \
      && sudo mv $TMPFILE /etc/pacman.d/mirrorlist \
      && yay-drop-caches \
      && yay -Syyu --noconfirm'
    ```
  
#### Setting Up SSH Access to the Local Machine

The local machine is the machine on which you just have installed Arch Linux.
1. On the local machine, start the SSH service to allow remote access:
   ```bash
   sudo systemctl enable --now sshd
   ```
   With `ip addr` you can check the IP address of the local machine.
2. On the local machine, enable public key authentication:
   ```bash
   sudo vim /etc/ssh/sshd_config
   ```
   - Ensure `PubkeyAuthentication yes` is set.
   Restart the SSH service to apply the changes:
   ```bash
   sudo systemctl restart sshd
   ```
2. On the remote machine, copy the public SSH key to the local machine:
   ```bash
   ssh-copy-id -i .ssh/id_ed25519.pub <USERNAME>@<remote-ip>
   ```
   Replace `<remote-ip>` with the IP address of the remote machine. If you have multiple keys, specify the correct one with `-i`.
3. Test the SSH connection:
   ```bash
   ssh -i .ssh/id_ed25519.pub <USERNAME>@<remote-ip>
   ```
4. Harden the security on the local machine by editing the SSH configuration file:
   ```bash
   sudo vim /etc/ssh/sshd_config
   ```
   - Disable root login by setting `PermitRootLogin no`.
   - Disable password authentication by setting `PasswordAuthentication no`.
   - Disable empty passwords by setting `PermitEmptyPasswords no`.
   - Limit authentication retries by setting `MaxAuthTries 3`.
   - Disable X11 forwarding by setting `X11Forwarding no`.
   - Check DNS hostnames by setting `UseDNS yes`.
   Restart the SSH service to apply the changes:
   ```bash
   sudo systemctl restart sshd
   ```

#### Install Desktop Environment

1. Install the desktop environment and necessary packages.
   ```bash
   yay -S xorg-server xorg-xinit qtile ttc-iosevka python-screeninfo
   ```
2. Install backend service by first installing the dependencies.
    ```bash
    yay -S valkey python-redis
    sudo systemctl enable --now valkey
    ```
    In case you do not want to use the default redis backend, you can set the following environment variables (make sure they are available before the backend service and the desktop environment starts):
    ```bash
    NBS_REDIS_HOST=localhost
    NBS_REDIS_PORT=6379
    NBS_REDIS_DB=1
    ```
    Get the latest version of the backend service:
    ```
    cd ~/repositories
    git clone git@github.com:nuunamnir/nuunamnir.backend-service.git
    ```
    Then activate the service.
    ```bash
    cd nuunamnir.backend-service
    mkdir -p ~/.local/share/systemd/user
    cp nuunamnir.backend.service ~/.local/share/systemd/user/
    systemctl --user enable --now nuunamnir.backend
    ```

### Display Calibration

1. Install the `displaycal` package.
    ```bash
    yay -S displaycal
    ```
2. Disable all "intelligent" or "automatic" color and brightness adjustment features of your monitor. For mobile computer screens, set the brightness such that the calibration device measures a brightness of around 120cd/m². As root run the following command to disable automatic brightness adjustment:
   ```bash
   echo 0 > /sys/class/backlight/intel_backlight/brightness
   ```
   Adjust the path according to your system if necessary and replace 0 with the desired brightness value; you might need to try several values to find the right one. You can check the maximum brightness value by running:
   ```bash
   cat /sys/class/backlight/intel_backlight/max_brightness
   ```
2. Run `displaycal` and follow the instructions to calibrate your display. In general I use the `sRGB` color profile and aim fo 120cd/m² brightness.
3. Copy the generated ICC profile to the system color profile directory.
   ```bash
   sudo cp ~/.local/share/icc/<profile_name>.icc ~/.config/icc/
   ```
   Replace `<profile_name>` with the actual name of the generated ICC profile.
4. Activate the ICC profile using the following command and adding it to the .xinitrc file.
   ```bash
   dispwin -d 1 -i ~/.config/icc/<profile_name>.icc
   ```
   Replace `<profile_name>` with the actual name of the generated ICC profile. Use the correct display number if you have multiple displays.
