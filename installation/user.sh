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
