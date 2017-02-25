from tornado import websocket, web, ioloop, template
import json
import os
from user import Player

player1 = Player('Piotrek','http://192.170.100.12')
player2 = Player('Pati','http://192.170.100.15')

print(player2)
cl = []

p1 = {
  "userName": "piotrek",
  "websocket": "http:192.170.122"
    }
p2= {
      "userName": "piotrek",
      "websocket": "http:192.170.122"
    }
websockets = []
players = [player1,player2]


class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("templates/index.html")


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
        self.write(json.dumps(players))
        self.finish()

    @web.asynchronous
    def get(self, *args):
        # print(self._dict__)
        self.write(json.dumps(players))
        self.finish()

    @web.asynchronous
    def post(self):
        pass


class ShowPlayers(web.RequestHandler):
    def data_received(self, chunk):
        pass


    def get(self):

        # create first user and append to a user list
       self.render("templates/players.html",players=players)


class AddQuiz(web.RequestHandler):
    def data_received(self, chunk):
        pass


    def get(self):

        # create first user and append to a user list
       self.render("templates/add_quiz.html")


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/json/players', GetPlayers),
    (r'/players', ShowPlayers),
    (r'/static/(.*)', web.StaticFileHandler, {'path': 'static/'}),
    (r'/add-quiz', AddQuiz),
])


if __name__ == '__main__':
    app.listen(8888)
ioloop.IOLoop.instance().start()
