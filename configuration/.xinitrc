#!/bin/sh
userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

setxkbmap -layout de

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

if [ "$HOSTNAME" = "nippur" ]; then
    dispwin -i .local/share/DisplayCAL/storage/1731\ #1\ 2023-05-27\ 18-53\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX/1731\ #1\ 2023-05-27\ 18-53\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX.icc
fi

if [ "$HOSTNAME" = "assur" ]; then
    dispwin -d 1 -i ~/.config/icc_profiles/LG.icc 
    dispwin -d 2 -i ~/.config/icc_profiles/Samsung.icc 
fi

# workaround to make hidden fules show up in gtk file chooser
dconf write /org/gtk/settings/file-chooser/show-hidden true
gsettings set org.gtk.Settings.FileChooser show-hidden true

numlockx on &
python ~/.config/qtile/sunlight.py &
qtile start
