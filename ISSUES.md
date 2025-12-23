# Issues

## Miscellaneous

- [ ] Add representative screenshots to `README.md`
- [x] Fix installation script
- [ ] Add missing dependencies (OS packages) to installation instructions/dependencies list
- [ ] Integrate wallpaper generation script
- [ ] Add screen lock feature
- [ ] Reference VM with dot files
- [ ] Change color names to something meaningful, also show dark theme colors

## Configurations

- [ ] Map all colors for `qutebrowser`
- [ ] Handle monitor plug/unplug events gracefully in `qtile`
- [ ] Add web-greeter to patch configuration
- [ ] Add plymouth to patch configuration
- [ ] Automate installation of web-greeter
- [ ] Automate installation of plymouth
- [ ] Automatically path README.md on color theme change


## Background Service

- [x] Monitor and display audio levles (`qtile` widget)
- [ ] Monitor screen recording/streaming status (`qtile` widget) and wallpaper change

## Bugs

- [ ] qtile uses additional resources if the configuration is reloaded
- [ ] Prevent monitor energy saving when running video in `qutebrowser`
- [x] picom has some strange effect on video and games (initial black screen)
    - (2025-12-07) resolved by changing the picom backend from `egl` to `glx`
- [x] x server(?) crashes when theme switches mode
    - (2025-12-21) resolved by switching from `pkill` to `qtile cmd-obj`
