class Player():
    """"""

    def __init__(self, userName, websocket):
        self.userName = userName
        self.websocket = websocket
        self.points = 0

    def addPoints(self, points):
        self.points += points