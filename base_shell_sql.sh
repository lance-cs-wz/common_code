#!/bin/bash
set -x
set -e

# mysql读最新的数据
sql_bin="mysql --host=raycloudtest.mysql.rds.aliyuncs.com --port=3306 --user=kuaimai --password=qTemX6MPAU2P --database kuaimai_data --default-character-set=utf8 -e "

function read_new_data_from_mysql()
{
    last_process_id=0
    sql_cmd="select * from kd_scs_chat_log where id > $last_process_id;"
    
    $sql_bin "$sql_cmd"
}

function run()
{
    read_new_data_from_mysql
}

run
