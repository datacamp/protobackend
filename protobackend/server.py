import tornado.ioloop
import tornado.web
from tornado.netutil import bind_unix_socket
from tornado.httpserver import HTTPServer
import json

class DispatchServer:
    def __init__(self, dispatch, socket_path = 'unix.socket'):
        self.app = tornado.web.Application([
            (r"/", MainHandler, dict(dispatch = dispatch)),
        ], debug = True)
        
        if isinstance(socket_path, int):
            self.server = self.app.listen(socket_path)
        else:
            self.server = HTTPServer(self.app)
            self.socket = bind_unix_socket(socket_path)
            self.server.add_socket(self.socket)

    def start(self):
        tornado.ioloop.IOLoop.current().start()

    def stop(self):
        self.server.stop()

    def __del__(self):
        self.stop()


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, dispatch):
        self.dispatch = dispatch

    def prepare(self):
        _type = self.request.headers.get("Content-Type", "")
        if _type.startswith("application/json"):
            self.json_args = json.loads(self.request.body.decode())
        else:
            self.json_args = None

    def put(self):
        out = self.dispatch(self.json_args)
        #self.write("Hello, world")
        self.write(json.dumps(out))

    def get(self):
        self.write('1')


