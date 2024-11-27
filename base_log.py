# -*- coding:utf-8 -*-
# Python version is 2.7
import os
import sys
import time

def log(log_text, log_name="Log", lineno=0):
    if lineno <= 0:
        lineno = sys._getframe().f_back.f_lineno

    now_time_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sys.stderr.write("%s  line:%4d  %s:  %s\n" % (now_time_text, lineno, log_name, log_text))


def info(info_text):
    log(info_text, "Info", sys._getframe().f_back.f_lineno)


def debug(debug_text):
    log(debug_text, "Debug", sys._getframe().f_back.f_lineno)


def warn(warn_text):
    log(warn_text, "Warning", sys._getframe().f_back.f_lineno)


def err(err_text):
    log(err_text, "Error", sys._getframe().f_back.f_lineno)
