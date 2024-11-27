# -*- coding:utf-8 -*-
# Python version is 2.7
import os
import re
import sys
import json
import time

import logging
import logging.config

import ConfigParser

import pymysql

logging.config.fileConfig("./logging_config.ini")
log = logging.getLogger()

now_time_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_db_cursor(config_file_path, db_config_name="base"):
    log.info("Start get_db_cursor")
    log.info("Get db cursor by config " + config_file_path)
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    
    log.info("Get cf %s: %s" % (db_config_name, str(cf.items(db_config_name))))

    host = cf.get(db_config_name, "host")
    port = cf.getint(db_config_name, "port")
    user = cf.get(db_config_name, "user")
    password = cf.get(db_config_name, "password")
    db_name = cf.get(db_config_name, "db_name")
    charset = cf.get(db_config_name, "charset")

    db = pymysql.connect(host, user, password, db = db_name, charset = charset, cursorclass = pymysql.cursors.SSCursor)

    return db, db.cursor()

if __name__ == "__main__":
    get_db_cursor("./db_config.ini")
