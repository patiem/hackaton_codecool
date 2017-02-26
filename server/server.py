from tornado import websocket, web, ioloop, template
import json
import os
from user import Player
from quiz import Quiz
from question import Question
from datetime import datetime



cl = []
playersSocket = []
p1 = {
    "userName": "piotrek",
    "beaconId": "1"

}
p2 = {
    "userName": "piotrek",
    "beaconId": "2"
}
websockets = []
players = []
playersSocket = [p1, p2]

class DecodeUser(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class IndexHandler(web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("templates/index.html")


class SocketHandler(websocket.WebSocketHandler):

    listForPoints = [['pati', 'a', datetime.today()], ['pati', 'b', datetime.today()]]  # where!!!!

    def data_received(self, chunk):
        print("get data chunk from " + self.request.remote_ip)

    def on_message(self, message):
        # print("get message from " + self.request.remote_ip + ": " + message)
        temp = DecodeUser(message)
        if "beaconId" not in temp.__dict__.keys():
            players.append(Player(temp.username, self.request.remote_ip))
        elif "beaconId" in temp.__dict__.keys():
            listForPoints.append([temp.username, temp.beaconId, datetime.today()])
            print(listForPoints)

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
        if int(answerId) > 1:
            print(SocketHandler.listForPoints)
            Question.check_answers(SocketHandler.listForPoints)
            
            SocketHandler.listForPoints = []

        if not self.questionList:
            self.questionList = Question.get_questions_by_id(quizId)

        self.render("templates/question.html", questions=self.questionList[int(answerId)-1],
                    max_id=len(self.questionList))


    """def post(self):
        print(StartQuiz.quizId)
        self.questionList = Question.get_questions_by_id(StartQuiz.quizId)
        self.render("templates/question.html")
        pass"""


class ShowEnd(web.RequestHandler):

    def get(self):

        self.render("templates/end.html")

    """def post(self):
        print(StartQuiz.quizId)
        self.questionList = Question.get_questions_by_id(StartQuiz.quizId)
        self.render("templates/question.html")
        pass"""




app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/json/players', GetPlayers),
    (r'/players', ShowPlayers),
    (r'/static/(.*)', web.StaticFileHandler, {'path': 'static/'}),
    (r'/add-quiz', AddQuiz),
    (r'/start', StartQuiz),
    (r'/one', ShowQuestion),
    (r'/end', ShowEnd),
])

if __name__ == '__main__':
    app.listen(8888)
ioloop.IOLoop.instance().start()
