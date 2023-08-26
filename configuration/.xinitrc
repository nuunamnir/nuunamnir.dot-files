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

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

if $HOSTNAME == "nippur"; then
    dispwin -i .local/share/DisplayCAL/storage/1731\ #1\ 2023-05-27\ 18-53\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX/1731\ #1\ 2023-05-27\ 18-53\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX.icc
else
    dispwin -d 1 -i ~/.config/icc_profiles/LG.icc 
    dispwin -d 2 -i ~/.config/icc_profiles/Samsung.icc 
fi

numlockx on &
# ~/repositories/nuunamnir.environment-services/venv/bin/python -m uvicorn serve:app --host 0.0.0.0 --port 2107 --app-dir ~/repositories/nuunamnir.environment-services/src/ &
qtile start
