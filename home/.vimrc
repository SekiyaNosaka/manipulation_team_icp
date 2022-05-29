" __   _( ) __ ___ 
" \ \ / / | '_ ` _ \
"  \ V /| | | | | | |
"   \_/ |_|_| |_| |_|


"--- General
set ruler
set smartindent
set expandtab
set tabstop=4
set shiftwidth=4
set virtualedit=onemore
set autoread
set clipboard=unnamed,autoselect
set noswapfile
filetype plugin indent on
inoremap <silent> jj <ESC>
autocmd BufNewFile,BufRead *.launch setf xml

"--- Visual
set number
set display=lastline
syntax enable
colorscheme deus

"--- Movement
"set whichwrap=b,s,h,l,<,>,[,],~

"--- Search
set hlsearch
set wrapscan
set ignorecase
set smartcase
set incsearch
nnoremap <ESC><ESC> :nohl<CR>

