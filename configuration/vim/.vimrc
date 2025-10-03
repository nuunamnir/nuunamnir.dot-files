" install plug plugin manager
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif


call plug#begin()
" list your plugins here
Plug 'tpope/vim-sensible'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'preservim/nerdtree'
Plug 'sheerun/vim-polyglot'
Plug 'https://github.com/github/copilot.vim'
call plug#end()


" some color theme configurations
highlight VertSplit cterm=None


" disable vi fallback compatibility
set nocompatible
set wildmenu

" rebind pane navigation
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l


" enable line numbers (hybrid)
set number relativenumber
" switch to absolute line numbers in insert mode
augroup numbertoggle
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave,WinEnter * if &nu && mode() != "i" | set rnu   | endif
  autocmd BufLeave,FocusLost,InsertEnter,WinLeave   * if &nu                  | set nornu | endif
augroup END


set encoding=utf-8
syntax on

" nerdtree configuration
nmap <C-f> :NERDTreeFind<CR>
" open nerdtree with the tree expanded to the opened file and focus opened
" file
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() > 0 || exists('s:std_in') | NERDTreeFind |  wincmd p | else | NERDTreeToggle | wincmd p |  endif

autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
