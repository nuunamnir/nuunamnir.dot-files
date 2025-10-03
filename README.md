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

The color scheme is designed to correlated lightness and chroma with perceptual saliency, allowing to assign certain meanings to the hue. More information of how these colors were selected can be found [here](https://www.github.com/nuunamnir/nuunamnir.color-scheme).

| Name            | sRGB String    | sRGB Numeric          | Patch |
|-----------------|---------------------|----------------| ----- |
| pastel_red      | `#c29b9b            ` | `(0.761, 0.608, 0.608)` | ![#c29b9b](assets/c29b9b.png) |
| negative        | `#fb8087            ` | `(0.984, 0.502, 0.529)` | ![#fb8087](assets/fb8087.png) |
| red             | `#dc9192            ` | `(0.863, 0.569, 0.573)` | ![#dc9192](assets/dc9192.png) |
| background      | `#ebebeb            ` | `(0.922, 0.922, 0.922)` | ![#ebebeb](assets/ebebeb.png) |
| light_muted     | `#d3d3d3            ` | `(0.827, 0.827, 0.827)` | ![#d3d3d3](assets/d3d3d3.png) |
| light_grey      | `#bcbcbc            ` | `(0.737, 0.737, 0.737)` | ![#bcbcbc](assets/bcbcbc.png) |
| cursor          | `#636363            ` | `(0.388, 0.388, 0.388)` | ![#636363](assets/636363.png) |
| dark_grey       | `#8e8e8e            ` | `(0.557, 0.557, 0.557)` | ![#8e8e8e](assets/8e8e8e.png) |
| foreground      | `#787878            ` | `(0.471, 0.471, 0.471)` | ![#787878](assets/787878.png) |
| dark_muted      | `#787878            ` | `(0.471, 0.471, 0.471)` | ![#787878](assets/787878.png) |
| grey            | `#a4a4a4            ` | `(0.643, 0.643, 0.643)` | ![#a4a4a4](assets/a4a4a4.png) |
| pastel_yellow   | `#b4a289            ` | `(0.706, 0.635, 0.537)` | ![#b4a289](assets/b4a289.png) |
| yellow          | `#bfa06e            ` | `(0.749, 0.627, 0.431)` | ![#bfa06e](assets/bfa06e.png) |
| effect_pastel   | `#a7a68a            ` | `(0.655, 0.651, 0.541)` | ![#a7a68a](assets/a7a68a.png) |
| neutral         | `#a5aa49            ` | `(0.647, 0.667, 0.286)` | ![#a5aa49](assets/a5aa49.png) |
| effect_bright   | `#eef18c            ` | `(0.933, 0.945, 0.549)` | ![#eef18c](assets/eef18c.png) |
| effect_muted    | `#a7a86f            ` | `(0.655, 0.659, 0.435)` | ![#a7a86f](assets/a7a86f.png) |
| effect_dark     | `#606900            ` | `(0.376, 0.412, 0.000)` | ![#606900](assets/606900.png) |
| positive        | `#6ab669            ` | `(0.416, 0.714, 0.412)` | ![#6ab669](assets/6ab669.png) |
| green           | `#84af81            ` | `(0.518, 0.686, 0.506)` | ![#84af81](assets/84af81.png) |
| pastel_green    | `#95aa93            ` | `(0.584, 0.667, 0.576)` | ![#95aa93](assets/95aa93.png) |
| cyan            | `#4bb4b7            ` | `(0.294, 0.706, 0.718)` | ![#4bb4b7](assets/4bb4b7.png) |
| pastel_cyan     | `#80adae            ` | `(0.502, 0.678, 0.682)` | ![#80adae](assets/80adae.png) |
| pastel_blue     | `#90a7bf            ` | `(0.565, 0.655, 0.749)` | ![#90a7bf](assets/90a7bf.png) |
| blue            | `#73aadb            ` | `(0.451, 0.667, 0.859)` | ![#73aadb](assets/73aadb.png) |
| magenta         | `#c097c8            ` | `(0.753, 0.592, 0.784)` | ![#c097c8](assets/c097c8.png) |
| pastel_magenta  | `#b39eb6            ` | `(0.702, 0.620, 0.714)` | ![#b39eb6](assets/b39eb6.png) |

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
    echo "KEYMAP=de-latin1" > /etc/vconsole.conf
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
