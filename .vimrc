set encoding=utf-8
set fileencodings=utf-8,gb2312,gbk,gb18030,big5

if has('win32')
set fileencoding=chinese
else
set fileencoding=utf-8
endif

set ts=4
set expandtab
%retab!

source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim
"解决consle输出乱码
language messages zh_CN.utf-8

set nu!
set ai!
set showmatch
set pastetoggle=<F9>
filetype on
syntax on
