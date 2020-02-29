import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket as ws
from tornado.options import define, options
import time

define('port', default=8500, help='port to listen on')

class web_socket_handler(ws.WebSocketHandler):
    '''
    This class handles the websocket channel
    '''

    @classmethod
    def route_urls(cls):
        return [(r'/', cls, {}), ]

    def simple_init(self):
        self.last = time.time()
        self.stop = False

    def open(self):
        '''
            client opens a connection
        '''
        self.simple_init()
        print("New client connected")
        self.write_message("You are connected")

    def on_message(self, message):
        '''
            Message received on the handler
        '''
        print("received message {}".format(message))
        self.write_message("You said {}".format(message))
        self.last = time.time()

    def on_close(self):
        '''
            Channel is closed
        '''
        print("connection is closed")
        self.loop.stop()

    def check_origin(self, origin):
        return True


def initiate_server():
    app = tornado.web.Application(web_socket_handler.route_urls())

    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    initiate_server()