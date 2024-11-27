#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process


PORT = 8090
PROCESS_COUNT = 8

class LongHandler(tornado.web.RequestHandler):

    def post(self):
        time.sleep(1)
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + str(os.getpid()) + ' ' + str(time.time()) + '\n')


    def get(self):
        self.write(str(os.getpid()))
        time.sleep(1)


if __name__ == "__main__":
    app = tornado.web.Application(([r'/', LongHandler], ))
    sockets = tornado.netutil.bind_sockets(PORT)
    tornado.process.fork_processes(PROCESS_COUNT)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()
