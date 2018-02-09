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

from handlers.ConnectingPathHandler import FindEdgeLabel, FindOutputHandler, MetaDataHandler, ConnectingPathHandler, EndpointHandler, ConnectingOutputHandler, ConnectingInputHandler, ApiMapHandler, ApiMapHandlerSankey, Input2EndpointHandler, KnowledgeMapEndpoint, KnowledgeMapInput, KnowledgeMap, KnowledgeMapPath, Endpoint2OutputHandler
from handlers.basehandler import BaseHandler


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", messages=None)

class APIHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("api.html", messages=None)

class TutorialHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("tutorial.html", messages=None)

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True,
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }
        handlers = [
            (r"/explorer/?", MainHandler),
            (r"/explorer/tutorial/?", TutorialHandler),
            (r"/explorer/api/?", APIHandler),
            (r"/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/tutorial/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/path", ConnectingPathHandler),
            (r"/explorer/input", ConnectingInputHandler),
            (r"/explorer/apimap", ApiMapHandler),
            (r"/explorer/output", ConnectingOutputHandler),
            (r"/explorer/endpoint", EndpointHandler),
            (r"/explorer/metadata/([^/]+)", MetaDataHandler),
            (r"/explorer/findoutput", FindOutputHandler),
            (r"/explorer/apimapsankey", ApiMapHandlerSankey),
            (r"/explorer/input2endpoint", Input2EndpointHandler),
            (r"/explorer/endpoint2output", Endpoint2OutputHandler),
            (r"/explorer/findedgelabel", FindEdgeLabel),
            (r"/explorer/knowledgemap/endpoint", KnowledgeMapEndpoint),
            (r"/explorer/knowledgemap/input", KnowledgeMapInput),
            (r"/explorer/knowledgemap", KnowledgeMap),
            (r"/explorer/knowledgemap/path", KnowledgeMapPath)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
