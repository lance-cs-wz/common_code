# set local

export HBASE_HOME=/data/project/public/hbase/hbase-1.4.3
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.171-3.b10.el6_9.x86_64
export HADOOP_HOME=/data/project/public/hbase/hadoop-3.1.0
export PATH=$PATH:/home/wangzhen/local/git/bin:${JAVA_HOME}/bin:${HBASE_HOME}/bin:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin
export HISTTIMEFORMAT="%F %T "

export LC_ALL='C'
export LANG="en_US.UTF-8"

RUBBISH=~/.rubbish
if [ ! -d $RUBBISH ]; then
    mkdir -p $RUBBISH
fi

alias c='clear'
alias h='history | tail -n 40'
alias j='jobs -l'
alias k='kill -9'
alias l='ls -lrt'
alias v='vim'

alias ce='crontab -e'
alias ch='chmod a+wrx -R'
alias cl='crontab -l'
alias cp='cp -rf'
alias du='du -sh'
alias hd='hadoop'
alias hs='hbase shell'
alias rf='readlink -f'
alias rm='mv -t $RUBBISH'
alias r='mv -t $RUBBISH'
alias rr='/bin/rm -rf'
alias rrr='/bin/rm -rf $RUBBISH/*'
alias vb='vim ~/.bashrc'
alias vv='vim ~/.vimrc'
alias sb='source ~/.bashrc'

alias py='python2.7'
alias py2='python2.7'
alias git2='~/local/git/bin/git'
alias git='git2'

alias screen='screen -U'

alias lsaf='ls -lR | grep "^-" | wc -l'

umask 000

ulimit -u 10000
ulimit -n 4096
ulimit -d unlimited
ulimit -m unlimited
ulimit -s unlimited
ulimit -t unlimited
ulimit -v unlimited
