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

from utils import field_handler, annotate_handler, query_handler, id_handler, initialize, filter_handler
 
class MainHandler(tornado.web.RequestHandler):
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

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/field/", FieldHandler),
            (r"/annotate/", AnnotateHandler),
            (r"/query/", QueryHandler),
            (r"/id/", IdHandler),
            (r"/initialize/", InitializeHandler),
            (r"/filter/", FilterHandler)
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8865)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()