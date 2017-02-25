from tornado import websocket, web, ioloop
import json

cl = []

websockets = []
players = []


class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class SocketHandler(websocket.WebSocketHandler):
    def data_received(self, chunk):
        print("get data chunk from " + self.request.remote_ip)

    def on_message(self, message):
        print("get message from " + self.request.remote_ip + ": " + message)
        players.append(message)

    def check_origin(self, origin):
        return True

    def open(self):
        print("opened socket with " + self.request.remote_ip)
        if self not in websockets:
            websockets.append(self)

    def on_close(self):
        print("closed socket with " + self.request.remote_ip)
        if self in websockets:
            websockets.remove(self)


class GetPlayers(web.RequestHandler):
    def data_received(self, chunk):
        pass

    @web.asynchronous
    def get(self, *args):
        self.write(json.dumps(players))
        self.finish()

    @web.asynchronous
    def post(self):
        pass


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api/v1.0/players', GetPlayers),
])

if __name__ == '__main__':
    app.listen(8888)
ioloop.IOLoop.instance().start()
