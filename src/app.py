import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import json
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.options import define, options
import requests

from handlers.ConnectingPathHandler import FindOutputHandler, MetaDataHandler, ConnectingPathHandler, EndpointHandler, ConnectingOutputHandler, ConnectingInputHandler, ApiMapHandler, ApiMapHandlerSankey
from handlers.basehandler import BaseHandler


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", messages=None)

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True,
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }
        handlers = [
            (r"/explorer/?", MainHandler),
            (r"/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/path", ConnectingPathHandler),
            (r"/explorer/input", ConnectingInputHandler),
            (r"/explorer/apimap", ApiMapHandler),
            (r"/explorer/output", ConnectingOutputHandler),
            (r"/explorer/endpoint", EndpointHandler),
            (r"/explorer/metadata/([^/]+)", MetaDataHandler),
            (r"/explorer/findoutput", FindOutputHandler),
            (r"/explorer/apimapsankey", ApiMapHandlerSankey)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
