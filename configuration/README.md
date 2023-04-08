# Arch Linux Configuration

## Usage

This directory represents your home directory with respect to configuration files. To use a particular configuration, create a symbolic link to the file or directory (replace .config-file by the desired file or directory name)
```
cd ~
ln -sn ~/repositories/nuunamnir.dot-files/configuration/.config-file .config-file
```

## Dependencies
### qtile
```yay -S nerd-fonts-meta feh tk python-screeninfo python-dbus-next picom-git```
