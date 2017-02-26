import sql

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

    def add_user_to_db(self):
        query_2 = """INSERT INTO `users` (`name`, `points`)
                             VALUES (?, ?)"""
        params = [self.name, self.points]
        sql.query(query_2, params)