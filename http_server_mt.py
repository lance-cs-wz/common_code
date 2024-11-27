#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re
import sys
import cgi
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

import knownledge_solution_order_get_proc
import knownledge_solution_order_post_proc

ip = ""
ser_port = 5771
access_control_allow_origin = "*"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


def parse_get_query(query):
    log.info("query is %s" % query)
    query = urllib.unquote(query)

    log.info("query is %s" % query)
    method, params = query.split("?")
    request_data_dict = {}
    for param in params.split("&"):
        k, v = param.split("=")
        request_data_dict[k] = v
    return method, request_data_dict


class ProHTTPHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Origin", access_control_allow_origin)
        self.send_header("Access-Control-Max-Age", "18000")
        self.end_headers()
        self.wfile.close()


    def set_send_header_for_each_method(self, method, request_data_dict):
        self.send_header("Access-Control-Allow-Origin", "*")

        if method == "getOrderSolution":
            file_name = "orderSolution.xls"
            if "fileName" in request_data_dict:
                file_name = request_data_dict["fileName"]
            self.send_header("Content-Disposition", "attachment;filename=%s" % file_name)
            self.send_header("Content-Type", "application/octet-stream")

        self.end_headers()


    def do_GET(self):
        # 修改代码不用重启服务
        reload(knownledge_solution_order_get_proc)

        query = self.path[1: ]
        method, request_data_dict = parse_get_query(query)
        log.info("request_data_dict is %s" % (json.dumps(request_data_dict, ensure_ascii=False, indent=2).encode("utf-8")))
        out, result, message = knownledge_solution_order_get_proc.get_get_result(method, request_data_dict)

        self.send_response(200)
        self.set_send_header_for_each_method(method, request_data_dict)
        self.wfile.write(out)
        self.wfile.close()


    def do_POST(self):
        
        # 修改代码不用重启服务
        reload(knownledge_solution_order_post_proc)
        st_time_post = time.time()
        method = self.path[1: ]

        out_data = ""

        out_dict = {}
        out_dict["apiName"] = "chatLogSeach"
        out_dict["data"] = {}
        out_dict["message"] = ""
        out_dict["result"] = 100
        out_dict["subCode"] = 0

        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", access_control_allow_origin)
        request_data_str = ""

        try:
            if method == "updateAnsPic":
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                postvars = cgi.parse_multipart(self.rfile, pdict)
                file_content = ""
                for content in postvars["file"]:
                    file_content += content

                self.send_header("Content-Type", "application/json;charset=utf-8")
                out_dict["data"], out_dict["result"], out_dict["message"] = knownledge_solution_order_post_proc.get_post_result(method, file_content)
                out_data = json.dumps(out_dict, ensure_ascii=False).encode("utf-8")

            else:
                request_data_str = self.rfile.read(int(self.headers['content-length']))
                request_data_decode = urllib.unquote(request_data_str)
                log.info(str(request_data_str)[:4096])

                if method == "getOrderSolution":
                    out_data, result, message = knownledge_solution_order_get_proc.get_get_result(method, json.loads(request_data_str))
                    self.set_send_header_for_each_method(method, json.loads(request_data_str))

                else:
                    self.send_header("Content-Type", "application/json;charset=utf-8")
                    out_dict["data"], out_dict["result"], out_dict["message"] = knownledge_solution_order_post_proc.get_post_result(method, request_data_str)
                    out_data = json.dumps(out_dict, ensure_ascii=False).encode("utf-8")
        except:
            self.send_header("Content-Type", "application/json;charset=utf-8")
            out_dict["result"] = 200
            out_dict["message"] = "something error"
            log.error("something error")
            out_data = json.dumps(out_dict, ensure_ascii=False).encode("utf-8")

        self.end_headers()
        self.wfile.write(out_data)
        self.wfile.close()

        ed_time_post = time.time()
        used_time = ed_time_post - st_time_post

        log_text = "ip:%s:%s\trequest_data_str:%s\tused_time:%d" % (self.client_address[0], self.client_address[1], str(request_data_str)[:4096], used_time)
        log.info(log_text)


def start_server(port=8011):
    http_server = ThreadedHTTPServer(('', int(port)), ProHTTPHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ser_port = int(sys.argv[1])
    start_server(ser_port)
