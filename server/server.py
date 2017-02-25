from tornado import websocket, web, ioloop, template
import json
import os
from user import Player
from quiz import Quiz
from question import Question

player1 = Player('Piotrek', 'http://192.170.100.12')
player2 = Player('Pati', 'http://192.170.100.15')

print(player2)
cl = []
playersSocket = []
p1 = {
    "userName": "piotrek",
    "websocket": "http:192.170.122"
}
p2 = {
    "userName": "piotrek",
    "websocket": "http:192.170.122"
}
websockets = []
players = [player1, player2]


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
        playersSocket.append(message)

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
        # print(self._dict__)
        self.write(json.dumps(playersSocket))
        self.finish()

    @web.asynchronous
    def post(self):
        pass


class ShowPlayers(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        # create first user and append to a user list
        self.render("templates/players.html", players=players)


class AddQuiz(web.RequestHandler):

    questionAmount = 3

    def data_received(self, chunk):
        pass

    def get(self):
        # create first user and append to a user list
        self.render("templates/add_quiz.html", amount=self.questionAmount)

    def post(self):
        question_text = self.get_argument('question_text', '')
        url_img = self.get_argument('url_img', '')
        a_1 = self.get_argument("a_1", "")
        a_2 = self.get_argument("a_2", "")
        print(question_text, url_img, a_1, a_2)

class StartQuiz(web.RequestHandler):

    quizList = Quiz.get_quiz_list()
    quizId = None


    def data_received(self, chunk):
        pass

    def get(self):
        self.render("templates/start.html", quizes=self.quizList)

    def post(self):
        pass


class ShowQuestion(web.RequestHandler):

    questionList = [] #  Question.get_questions_by_id(StartQuiz.quizId)

    def get(self):
        quizId = self.get_argument('user_choice', '')
        answerId = self.get_argument('answer', '')
        print(answerId)
        if not self.questionList:
            self.questionList = Question.get_questions_by_id(quizId)
        self.render("templates/question.html", questions=self.questionList[int(answerId)-1],
                    max_id=len(self.questionList))

    def post(self):
        print(StartQuiz.quizId)
        self.questionList = Question.get_questions_by_id(StartQuiz.quizId)
        self.render("templates/question.html")
        pass

    #     self.quizId = self.get_argument('user_choice', '')
    #     print(self.quizId)




app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/json/players', GetPlayers),
    (r'/players', ShowPlayers),
    (r'/static/(.*)', web.StaticFileHandler, {'path': 'static/'}),
    (r'/add-quiz', AddQuiz),
    (r'/start', StartQuiz),
    (r'/one', ShowQuestion)  #, {'path': 'question/'}),
])

if __name__ == '__main__':
    app.listen(8888)
ioloop.IOLoop.instance().start()
