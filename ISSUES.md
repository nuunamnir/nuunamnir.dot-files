# Issues and Ideas
A list of issues and ideas.

## Theme
* allow for light and dark theme
    * ~~automatically update kitty (explore themes)~~
    * automatically update gtk
    * fix long loading delay due to querying the requests
* gtk add font size (might not be necessary, could be a bug of [VSC](https://github.com/microsoft/vscode/issues/151803))

## Keyboard
* show of function keys are enabled
* some keyboard shortcut switches keyboard layout - needs to fixed

## Other
* show which output device is used for audio (define a default)
* show which bluetooth devices are connected (and if available their remaining battery charge)
* configure dunst (notification service)
* configure starship (shell prompt)
* share edid / document how to generate
* share icc / document how to generate
* install script
* gtk color theme - dark/bright ( partially resolved, added the setting - but is not dynamically set)
* handle monitors being plugged in or plugged out while qtile is running
* show prompt on focused screen
* open app on screen from which the command was issued



## Resolved
* ~~show hidden files in file manager~~ (resolved by editing the gtk config)
* ~~numlock as default state~~ (resolved by adding numlockx - it was working, but qtile/xorg turns numlock off - in terminal it was on)
* ~~floating window border~~ (resolved by adding the border arguments to the floating_layout that was already present in the qtile config)
* ~~qtile groupbox urgent text(?) follow color theme~~ (resolved by adding the urgent* arguments to the groupbox widget)
* ~~add default theme~~ (resolved by adding spaceinvaders-inspired wallpapers)
* ~~update theme generator~~ (resolved by adding own wallpaper to documentation)
    * ~~add additional colors~~ (resolved by adding 16 foreground-accent/background-accent derived colors)