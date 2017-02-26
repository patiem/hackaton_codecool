class Player():
    """"""

    def __init__(self, userName, websocket):
        self.userName = userName
        self.websocket = websocket
        self.points = 0
        self.ready = True

    def addPoints(self, points):
        self.points += points

    def setReady(self, state):
        self.ready += state