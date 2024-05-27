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
alias code='code --enable-proposed-api ms-python.python --enable-proposed-api ms-toolsai.jupyter --enable-proposed-api GitHub.copilot'

eval "$(starship init zsh)"
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
