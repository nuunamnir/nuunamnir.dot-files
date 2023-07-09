[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

alias code='code --enable-proposed-api ms-python.python --enable-proposed-api ms-toolsai.jupyter --enable-proposed-api GitHub.copilot'

alias yay-drop-caches='sudo paccache -rk3; yay -Sc --aur --noconfirm'
alias yay-update-all='export TMPFILE="$(mktemp)"; \
	sudo true; \
	rate-mirrors --entry-country=DE --save=$TMPFILE arch --max-delay=21600 \
	&& sudo mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup \
	&& sudo mv $TMPFILE /etc/pacman.d/mirrorlist \
	&& yay-drop-caches \
	&& yay -Syyu --noconfirm'


PS1='[\u@\h \W]\$ '

export QT_AUTO_SCREEN_SCALE_FACTOR=0 

eval "$(starship init bash)"
