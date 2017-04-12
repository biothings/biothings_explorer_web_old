import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import json
import pprint
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.options import define, options

from utils import field_handler, annotate_handler, query_handler, id_handler, initialize, filter_handler, relation_handler, fetchid_handler
 
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", messages=None)

class FieldHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        # new dictionary
        response_to_send = field_handler(json_obj)

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

class AnnotateHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        # new dictionary
        response_to_send = annotate_handler(json_obj)

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

class QueryHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        # new dictionary
        response_to_send = query_handler(json_obj)

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

class IdHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        # new dictionary
        response_to_send = id_handler(json_obj)

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

class InitializeHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        # new dictionary
        response_to_send = initialize(json_obj['type'], json_obj['id'])

        print('Response to return')

        pprint.pprint(response_to_send)

        self.write(json.dumps(response_to_send))

class FilterHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        response_to_send = filter_handler(json_obj)
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))

class RelationHandler(tornado.web.RequestHandler):

    def post(self):
        response_to_send = relation_handler()
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))

class FetchIdHandler(tornado.web.RequestHandler):
    def post(self):
        response_to_send = fetchid_handler()
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/explorer/?", MainHandler),
            (r"/explorer/field/", FieldHandler),
            (r"/explorer/annotate/", AnnotateHandler),
            (r"/explorer/query/", QueryHandler),
            (r"/explorer/id/", IdHandler),
            (r"/explorer/initialize/", InitializeHandler),
            (r"/explorer/filter/", FilterHandler),
            (r"/explorer/relation/", RelationHandler),
            (r"/explorer/fetchid/", FetchIdHandler)
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
