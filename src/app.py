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
from raven import Client

from handlers.ConnectingPathHandler import FindEdgeLabel, FindOutputHandler, ConnectingPathHandler, ApiMapHandler, ApiMapHandlerSankey, KnowledgeMap, KnowledgeMapPath, ConnectingSemanticToIDHandler
from handlers.entitycrawler import Crawler
from handlers.basehandler import BaseHandler
from handlers.DirectPathHandler import DirectPathHandler
from handlers.DirectInput2OutputHandler import DirectInput2OutputHandler
from handlers.FindSynonymHandler import SynonymHandler
from handlers.SemanticQueryHandler import QuerySemanticsHandler
from handlers.MetaDataHandler import ConnectingInputHandler, EndpointHandler, ConnectingOutputHandler, ConnectingSemanticTypesHandler, MetaDataHandler
from handlers.APIStatusHandler import APIStatusHandler, DatabaseStatusHandler
from handlers.URIHandler import BioThingsURIHandler
from handlers.RegistryHandler import RegistryHandler
from handlers.MultiEdgeHandler import MultiEdgeHandler

client = Client('https://9dd387ee33954e9887ef4a6b55c7aa29:d98404d6199a4db1aa9b5a1e9fc3c975@sentry.io/294205')


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("explorer_new.html", messages=None)

class APIHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("api.html", messages=None)

class TutorialHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("tutorial.html", messages=None)

class CrawlerHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("crawler.html", messages=None)

class ExplorerHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("explorer.html", messages=None)

class MetaDataWebHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("metadata.html", messages=None)

class SourcesWebHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("sources.html", messages=None)

class RegistryWebHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("registry.html", messages=None)

class NavigatorHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("navigator.html", messages=None)

class ExplorerNewHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("explorer_new.html", message=None)

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True,
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }
        handlers = [
            (r"/explorer/?", MainHandler),
            (r"/explorer/new/?", ExplorerNewHandler),
            (r"/explorer/tutorial/?", TutorialHandler),
            (r"/explorer/api/?", APIHandler),
            (r"/explorer/explorer/?", ExplorerHandler),
            (r"/explorer/new/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/tutorial/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/crawler/?", CrawlerHandler),
            (r"/explorer/crawler/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/metadata/?", MetaDataWebHandler),
            (r"/explorer/sources/?", SourcesWebHandler),
            (r"/explorer/uri/?", RegistryWebHandler),
            (r"/explorer/metadata/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/uri/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/sources/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/navigator/?", NavigatorHandler),
            (r"/explorer/navigator/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/path", ConnectingPathHandler),
            (r"/explorer/apimap", ApiMapHandler),
            (r"/explorer/findoutput", FindOutputHandler),
            (r"/explorer/apimapsankey", ApiMapHandlerSankey),
            #(r"/explorer/input2endpoint", Input2EndpointHandler),
            #(r"/explorer/endpoint2output", Endpoint2OutputHandler),
            (r"/explorer/findedgelabel", FindEdgeLabel),
            (r"/explorer/api/v2/input", ConnectingInputHandler),
            (r"/explorer/api/v2/output", ConnectingOutputHandler),
            (r"/explorer/api/v2/endpoint", EndpointHandler),
            (r"/explorer/api/v2/knowledgemap", KnowledgeMap),
            (r"/explorer/api/v2/apigraph", KnowledgeMap),
            (r"/explorer/api/v1/path", KnowledgeMapPath),
            (r"/explorer/api/v2/metadata/([^/]+)", MetaDataHandler),
            (r"/explorer/vocab/terms/([.*]+)", BioThingsURIHandler),
            (r"/explorer/api/v2/findpath", KnowledgeMapPath),
            (r"/explorer/api/v2/crawler", Crawler),
            (r"/explorer/api/v2/directoutput", DirectPathHandler),
            (r"/explorer/api/v2/findsynonym", SynonymHandler),
            (r"/explorer/api/v2/directinput2output", DirectInput2OutputHandler),
            (r"/explorer/api/v2/semantic2id", ConnectingSemanticToIDHandler),
            (r"/explorer/api/v2/findsingleedge", DirectInput2OutputHandler),
            (r"/explorer/api/v2/semanticquery", QuerySemanticsHandler),
            (r"/explorer/api/v2/connectsemantictype", ConnectingSemanticTypesHandler),
            (r"/explorer/api/v2/multiedge", MultiEdgeHandler),
            (r"/explorer/api/v2/apistatus", APIStatusHandler),
            (r"/explorer/api/v2/databasestatus", DatabaseStatusHandler),
            (r"/explorer/api/v2/registry", RegistryHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
