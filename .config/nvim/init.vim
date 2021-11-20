syntax on

set mouse=a
set noerrorbells
set tabstop=4 softtabstop=4
set shiftwidth=4
set expandtab
set smartindent
set nu
set nowrap
set smartcase
set noswapfile
set nobackup
set undodir=~/.vim/undodir
set undofile
set incsearch
set termguicolors
set scrolloff=8

call plug#begin('~/.vim/plugged')
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'vim-airline/vim-airline'
Plug 'preservim/nerdtree'

" Plug 'gruvbox-community/gruvbox'
" Plug 'gilgilgilgil/anderson.vim'
" Plug 'Badacadabra/vim-archery'
" Plug 'wadackel/vim-dogrun'
" Plug 'colors/onedark.vim'
Plug 'joshdick/onedark.vim'
call plug#end()

colorscheme onedark
let g:coc_disable_startup_warning = 1
let g:airline_powerline_fonts = 1
highlight Normal guibg=none
highlight NonText guibg=none

" Auto NERDTree when launching NeoVim
" autocmd VimEnter * NERDTree | wincmd p
" autocmd Bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
