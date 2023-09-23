plugins=(sudo)

unalias -m '*'

alias yay-drop-caches='sudo paccache -rk3; yay -Sc --aur --noconfirm'
alias yay-update-all='export TMPFILE="$(mktemp)"; \
	sudo true; \
	rate-mirrors --entry-country=DE --save=$TMPFILE arch --max-delay=21600 \
	&& sudo mv /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup \
	&& sudo mv $TMPFILE /etc/pacman.d/mirrorlist \
	&& yay-drop-caches \
	&& yay -Syyu --noconfirm'

eval "$(starship init zsh)"