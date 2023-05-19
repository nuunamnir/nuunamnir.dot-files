[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

alias code='code --enable-proposed-api ms-python.python --enable-proposed-api ms-toolsai.jupyter'

PS1='[\u@\h \W]\$ '

export QT_AUTO_SCREEN_SCALE_FACTOR=0 

eval "$(starship init bash)"