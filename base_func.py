# -*- coding:utf-8 -*-
import os
import re
import sys
import json
import time
import base64
import hashlib
import urllib

from datetime import timedelta, datetime

import logging
import logging.config

logging.config.fileConfig("./logging_config.ini")
log = logging.getLogger()


def get_day_by_temp_day_str(temp_no=-1):
    return (datetime.today() + timedelta(temp_no)).strftime('%Y-%m-%d')

def get_now_time_text():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def test_get_now_time_text():
    log.debug("get_now_time_text() is %s" % get_now_time_text())


def dict_to_json_str(data_dict, indent=4, ensure_ascii=False, coding="utf-8"):
    return json.dumps(data_dict, ensure_ascii=ensure_ascii, indent=indent).encode(coding)

def test_dict_to_json_str():
    log.debug("dict_to_json_str() is \n%s" % dict_to_json_str({"cid": 261705, "kimiItemPropName": u"商品卖点", "knowledgeIds": [1, 13]}))


def solr_date_to_time_stamp(solr_date):
    rslt = time.mktime(time.strptime(solr_date, '%Y-%m-%dT%H:%M:%SZ'))
    return int(rslt)

    
def time_stamp_to_solr_date(time_stamp):
    if time_stamp < 0:
        return "*"
    rslt = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%dT%H:%M:%SZ")
    return rslt

    
def get_binary_file_md5(bin_file):
    buffer_size = 1024 * 1024 # 1M缓存
    md5 = hashlib.md5()
    while True:
        file_data = bin_file.read(buffer_size)
        if not file_data:
            break
        else:
            md5.update(file_data)
    md5_str = md5.hexdigest()
    return md5_str

def test_get_binary_file_md5():
    file_name = "base_func.py"
    out = ""
    with open(file_name, "rb") as bf:
        out = get_binary_file_md5(bf)
    log.debug("test_get_binary_file_md5(%s) is %s" % (file_name, out))


"""
    将文本转为base64文本
"""
def get_safe_base64_str(text):
    return base64.urlsafe_b64encode(text.encode()).decode("utf-8")


"""
    将base64文本转为文本
"""
def get_url_from_safe_base64_str(b64_str):
    return base64.urlsafe_b64decode(b64_str).decode("utf-8")


"""
    判断一个字符串是不是任意一个数字
"""
NUM_PATTERN = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
def is_number(num):
    result = NUM_PATTERN.match(num)
    if result:
        return True
    return False


"""
    对自然数的四舍五入取整函数，
        1. round(n)函数的特性： round(2.5) = 2； round(3.5)=4
        2. int(n + 0.5) 取整方法的特性，n为整数时会有问题。2 -> 2.5 -> 3
        3. 负数情况下存在问题，需要n-0.5。
    输入：
        n   ：任意数字数值
"""
def fixed_round(n):
    if n == int(n):
        return n
    if n < 0:
        return int(n - 0.5)
    return int(n + 0.5)


def get_post(url, data, headers = {'Content-Type': 'application/json'}):
    data = json.dumps(data)
    req = urllib.Request(url, data, headers)
    r = urllib.urlopen(req)
    return r.read()


def print_obj_attr_value(obj):
    for name in dir(obj):
        print("%-20s: %s" % (name, getattr(obj, name)))


def main(argv, argn):
    # test_get_day_by_temp_day_str()
    # test_get_now_time_text()
    # test_dict_to_json_str()
    test_get_binary_file_md5()
    return 0

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))

