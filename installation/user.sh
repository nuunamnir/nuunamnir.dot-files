#!/bin/bash

# Install these dot files.
mkdir repositories
cd repositories
git clone https://github.com/nuunamnir/nuunamnir.dot-files.git
cd
ln -s ~/repositories/nuunamnir.dot-files/configuration/.config .config

# Installs yay.
cd repositories
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Install rate-mirrors.
yay -S pacman-contrib rate-mirrors

# Install starship.
cd
yay -S otf-firamono-nerd ttf-firacode-nerd starship
rm .zshrc
ln -s ~/repositories/nuunamnir.dot-files/configuration/.zshrc .zshrc

# Install qtile.
yay -S xorg-server xorg-xinit numlockx kitty python-screeninfo python-dbus-next python-pydbus qtile
