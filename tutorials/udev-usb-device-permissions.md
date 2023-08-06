# Set Device Permissions with udev
## Description
Give automatically access to an USB device when it is plugged in without using sudo.
## Process
1. Identify the USB device and note the `idVendor` and `idProduct` from following output:
```
lsusb -vvv
```
2. Create a udev rule:
```
sudo vi /etc/udev/rules.d/50-usb.rules
```
With following content:
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="yyyy", GROUP="users", MODE="0666"
```
Replaying xxxx with the `idVendor` and yyyy with the `idProduct` respectively. Usually these identifiers are in hexadecimal format, e.g., 0x1234.

3. Reload the udev rules (sometimes a restart is required):
```
sudo udevadm control --reload
```
## References
+ [Source](https://www.xmodulo.com/change-usb-device-permission-linux.html)