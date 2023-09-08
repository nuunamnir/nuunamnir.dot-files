# udev Rules
## Usage
Copy these rules in `/etc/udev/rules.d/`. Run `udevadm verify` to check if problems with the rules. Reboot computer.
## Details
* 40-backlight.rules allows write access to backlight, add user to video group