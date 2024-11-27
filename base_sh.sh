#!/bin/bash
set -x
set -e

function init()
{
    ### 脚本通用配置
    work_path=/data/project/public
    py_bin="/usr/local/bin/python2.7"
    
    conf_path=./conf
    conf_path=`readlink -f $conf_path`
    data_path=./data
    data_path=`readlink -f $data_path`
    
    processing_flag_file=$conf_path/processing.flag
    
    ### 这次运行时的配置
    run_path=`pwd`
    
    run_date=`date "+%Y-%m-%d_%H:%M:%S"`
    run_day=`date "+%d"`
    run_time=`date "+%H_%M_%S"`
    
    run_data_dir=$data_path/$run_day/$run_time
    
    ### 脚本处理
    # 在以下代码中，不建议任何在函数之外出现的操作，除了run
    
    if [ $debug -eq 0 ]; then
        # 如果上次没跑完（正在运行或者异常退出），则不进行处理，并发出警报
        if [ -f $processing_flag_file ]; then
            echo "当前存在正在运行任务"
            # TODO 发邮件警报
            exit 0
        fi
    fi
}

function start()
{
    if [ -d $conf_path ]; then
        echo "conf_path $conf_path already exist." >/dev/stderr
    else
        mkdir -p $conf_path
    fi

    if [ -d $data_path ]; then
        echo "data_dir $data_path already exist." >/dev/stderr
    else
        mkdir -p $data_path
    fi

    if [ $debug -eq 0 ]; then
        # 如果上次没跑完（正在运行或者异常退出），则不进行处理，并发出警报
        if [ -f $processing_flag_file ]; then
            echo "当前存在正在运行任务"
            # TODO 发邮件警报
            exit 0
        fi
        > $processing_flag_file
    fi

    if [ -d $run_data_dir ]; then
        echo "run_data_dir $run_data_dir already exist." >/dev/stderr
    else
        mkdir -p $run_data_dir
    fi
}

function end()
{
    if [ -f $processing_flag_file ]; then
        rm $processing_flag_file
    fi
}

function do_something()
{
    # do_something
}

function run()
{
    debug=0

    init
    
    start

    do_something

    end
}

run
