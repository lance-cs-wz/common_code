#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re
import sys
import time
import json
import urllib
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

import logging
import logging.config

logging.config.fileConfig("./logging_config.ini")
log = logging.getLogger()

import knownledge_solution_order_proc

ip = ""
ser_port = 5771
access_control_allow_origin = "*"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


class ProHTTPHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Origin", access_control_allow_origin)
        self.send_header("Access-Control-Max-Age", "18000")
        self.end_headers()
        self.wfile.close()


    def do_POST(self):
        
        # 修改代码不用重启服务
        reload(knownledge_solution_order_proc)
        st_time_post = time.time()

        request_data = self.rfile.read(int(self.headers['content-length']))
        request_data_decode = urllib.unquote(request_data)
        log.info(request_data)

        out_dict = {}
        out_dict["apiName"] = "chatLogSeach"
        out_dict["data"] = {}
        out_dict["message"] = ""
        out_dict["result"] = 100
        out_dict["subCode"] = 0


        method = self.path[1: ]
        out_dict["data"], out_dict["result"], out_dict["message"] = knownledge_solution_order_proc.get_post_result(method, request_data)
        out_data = json.dumps(out_dict, ensure_ascii=False).encode("utf-8")
        # log.info(out_data)

        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", access_control_allow_origin)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.end_headers()
        self.wfile.write(out_data)
        self.wfile.close()

        ed_time_post = time.time()
        used_time = ed_time_post - st_time_post

        log_text = "ip:%s:%s\trequest_data:%s\tused_time:%d" % (self.client_address[0], self.client_address[1], request_data, used_time)
        log.info(log_text)


def start_server(port=8011):
    http_server = ThreadedHTTPServer(('', int(port)), ProHTTPHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ser_port = int(sys.argv[1])
    start_server(ser_port)
