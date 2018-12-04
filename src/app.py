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
            (r"/explorer_beta/?", MainHandler),
            (r"/explorer_beta/new/?", ExplorerNewHandler),
            (r"/explorer_beta/tutorial/?", TutorialHandler),
            (r"/explorer_beta/api/?", APIHandler),
            (r"/explorer_beta/explorer/?", ExplorerHandler),
            (r"/explorer_beta/new/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/tutorial/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/crawler/?", CrawlerHandler),
            (r"/explorer_beta/crawler/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/metadata/?", MetaDataWebHandler),
            (r"/explorer_beta/sources/?", SourcesWebHandler),
            (r"/explorer_beta/uri/?", RegistryWebHandler),
            (r"/explorer_beta/metadata/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/uri/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/sources/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/navigator/?", NavigatorHandler),
            (r"/explorer_beta/navigator/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer_beta/path", ConnectingPathHandler),
            (r"/explorer_beta/apimap", ApiMapHandler),
            (r"/explorer_beta/findoutput", FindOutputHandler),
            (r"/explorer_beta/apimapsankey", ApiMapHandlerSankey),
            #(r"/explorer/input2endpoint", Input2EndpointHandler),
            #(r"/explorer/endpoint2output", Endpoint2OutputHandler),
            (r"/explorer_beta/findedgelabel", FindEdgeLabel),
            (r"/explorer_beta/api/v2/input", ConnectingInputHandler),
            (r"/explorer_beta/api/v2/output", ConnectingOutputHandler),
            (r"/explorer_beta/api/v2/endpoint", EndpointHandler),
            (r"/explorer_beta/api/v2/knowledgemap", KnowledgeMap),
            (r"/explorer_beta/api/v2/apigraph", KnowledgeMap),
            (r"/explorer_beta/api/v1/path", KnowledgeMapPath),
            (r"/explorer_beta/api/v2/metadata/([^/]+)", MetaDataHandler),
            (r"/explorer_beta/vocab/terms/([.*]+)", BioThingsURIHandler),
            (r"/explorer_beta/api/v2/findpath", KnowledgeMapPath),
            (r"/explorer_beta/api/v2/crawler", Crawler),
            (r"/explorer_beta/api/v2/directoutput", DirectPathHandler),
            (r"/explorer_beta/api/v2/findsynonym", SynonymHandler),
            (r"/explorer_beta/api/v2/directinput2output", DirectInput2OutputHandler),
            (r"/explorer_beta/api/v2/semantic2id", ConnectingSemanticToIDHandler),
            (r"/explorer_beta/api/v2/findsingleedge", DirectInput2OutputHandler),
            (r"/explorer_beta/api/v2/semanticquery", QuerySemanticsHandler),
            (r"/explorer_beta/api/v2/connectsemantictype", ConnectingSemanticTypesHandler),
            (r"/explorer_beta/api/v2/multiedge", MultiEdgeHandler),
            (r"/explorer_beta/api/v2/apistatus", APIStatusHandler),
            (r"/explorer_beta/api/v2/databasestatus", DatabaseStatusHandler),
            (r"/explorer_beta/api/v2/registry", RegistryHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
