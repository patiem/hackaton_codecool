import sql

class Quiz:

    def __init__(self, title, quiz_id):
        self.title = title
        self.quiz_id = quiz_id

    @classmethod
    def add_quiz(cls, title):
        query = "SELECT max(ID) FROM QUIZ"
        new_id = sql.query(query)[0]
        new_quiz = cls(title, new_id)
        query_2 = """INSERT INTO QUIZ (title) VALUES (?)"""
        params = [title]
        sql.query(query_2, params)



Quiz.add_quiz('dupa')