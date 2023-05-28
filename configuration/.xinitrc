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
    dispwin -d 1 -i .local/share/DisplayCAL/storage/HDR\ 4K\ #1\ 2023-05-26\ 19-01\ 0.3127x\ 0.329y\ Rec.\ 1886\ F-S\ XYZLUT+MTX/HDR\ 4K\ #1\ 2023-05-26\ 19-01\ 0.3127x\ 0.329y\ Rec.\ 1886\ F-S\ XYZLUT+MTX.icc
    dispwin -d 2 -i .local/share/DisplayCAL/storage/S27B550\ #2\ 2023-05-26\ 17-49\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX/S27B550\ #2\ 2023-05-26\ 17-49\ 0.3127x\ 0.329y\ Rec.\ 1886\ M-S\ XYZLUT+MTX.icc
fi

qtile start
