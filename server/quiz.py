import sql

class Quiz:

    def __init__(self, title, quiz_id, questions=None):
        """
        :param title: string (title of quiz)
        :param quiz_id: int (id from DB)
        :param questions: list (list with questions_id)
        """
        self.title = title
        self.quiz_id = quiz_id
        if questions:
            self.questions = questions
        else:
            self.questions = []

    @classmethod
    def add_quiz(cls, title):
        query = "SELECT max(ID) FROM QUIZ"
        new_id = sql.query(query)[0][0] + 1
        print(new_id)
        new_quiz = cls(title, new_id)
        query_2 = """INSERT INTO QUIZ (title) VALUES (?)"""
        params = [title]
        sql.query(query_2, params)
        return new_quiz


    @classmethod
    def get_quiz_list(cls):
        query = "SELECT * FROM QUIZ"
        q_list = sql.query(query)
        list_to_send = []
        for item in q_list:
            quiz_id = item['id']
            title = item['title']
            list_to_send.append([quiz_id, title])
            cls(title, quiz_id)
        return list_to_send


    def add_question_to_quiz(self):
        pass

    def __str__(self):
        return '{}-{}'.format(self.title, self.quiz_id)


"""print(Quiz.add_quiz('dupa'))
Quiz.get_quiz_list()"""