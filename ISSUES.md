# Issues and Ideas
A list of issues and ideas.

## Keyboard
* some keyboard shortcut switches keyboard layout - needs to fixed

## Other
* use nvidia PRIME (to save battery?)
* automatically update system time depending on location, add timezone update to sunlight.py
* bluetooth widget should be hidden when not used
* show internet status
* understand timeshift
* add firefox to config handling
* problem with permissions on mirrorlist
* bluetooth headset does not connect if pavucontrol/firefox is not started beforehand
* fix cursor size on qtile
* add git colors to obey theme
* add .dir_colors to obey theme
* refactor qtile config    
* mouse cursor scaling not working on qtile
* integrating Visual Studio Code into config management
* show which output device is used for audio (define a default)
    * add mute key
* share edid / document how to generate
* install script
* handle monitors being plugged in or plugged out while qtile is running
* open app on screen from which the command was issued

## Resolved
* ~~Inkscape icons do not scale according to DPI~~ (resolved by changing the preference setting icon scale)
* ~~Firefox does not scale according to DPI~~ (resolved by changing about:config layout.css.devPixelsPerPx property to 0.8)
* ~~fix broken kitty configuration~~ (resolved by fixing console font scaling factor - kitty does not like font_size > 32)
* ~~handle different systems not based on node but on hostname~~ (resolved by replacing uuid.getnode by os.uname)
* ~~update debug to remove old log files~~ (resolved by adding the possibility to only retain n newest log files)
* ~~show which bluetooth devices are connected (and if available their remaining battery charge)~~ (resolved by adding the battery attribute to bluetooth widget; implemented a Logitech widget based on [solaar](https://pwr-solaar.github.io/Solaar/) - new installations required udev rule copy)
* ~~add rofi to config handling~~ (resolved by adding rofi to patch.py)
* ~~show prompt on focused screen~~ (resolved by switching from prompt widget to rofi)
* ~~show battery state on mobile computers~~ (added widget)
* ~~refactor theme generator~~ (updated [theme generator script](https://github.com/nuunamnir/nuunamnir.qtile-theme-generator))
* ~~recalibrate monitors (full brightness on mobile computer)~~ (performed recalibration)
* ~~share icc / document how to generate~~ (resolved by adding a README.md to the icc_profiles directory)
* ~~gtk color theme - dark/bright~~ (resolved, added a patch function for gtk setting)
* ~~show hidden files in file manager (seems to be a [bug](https://github.com/electron/electron/issues/34706)~~ - workaround implemented)
* ~~automatically update gtk~~ (resolved by adding a patch script)
* ~~add a theme debug log~~ (resolved by adding a simple debugger class)
* ~~show of function keys are enabled~~ (cannot be resolved, Fn keys is handled by keyboard controller and is not exposed to the os)
* ~~configure starship (shell prompt)~~ (resolved by adding a patch script)
* ~~gtk add font size (might not be necessary, could be a bug of [VSC](https://github.com/microsoft/vscode/issues/151803))~~ (resolved by changing the setting Windows > Title Bar Style to custom)
* ~~configure dunst (notification service)~~ (resolved by adding a patch script)
* ~~OS keyring for VSC~~ (resolved by adding "password-store":"gnome" to VSC runtime arguments)
* ~~qtile issue when reloading config (failed to reschedule)~~ (resolved by rewriting the sunlight service)
* ~~allow for light and dark theme~~
    * ~~automatically update kitty (explore themes)~~ (resolved by adding a theme file)
    * ~~fix long loading delay due to querying the requests~~ (resolved by adding a service to get sun stats in a subprocess)
* ~~refactor theme handling~~ (resolved by making use of the default theme)
* ~~refactor kitty theme handling~~ (resolved by creating a kitty class)
* ~~show hidden files in file manager~~ (resolved by editing the gtk config)
* ~~numlock as default state~~ (resolved by adding numlockx - it was working, but qtile/xorg turns numlock off - in terminal it was on)
* ~~floating window border~~ (resolved by adding the border arguments to the floating_layout that was already present in the qtile config)
* ~~qtile groupbox urgent text(?) follow color theme~~ (resolved by adding the urgent* arguments to the groupbox widget)
* ~~add default theme~~ (resolved by adding spaceinvaders-inspired wallpapers)
* ~~update theme generator~~ (resolved by adding own wallpaper to documentation)
    * ~~add additional colors~~ (resolved by adding 16 foreground-accent/background-accent derived colors)