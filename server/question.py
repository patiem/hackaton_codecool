import sql


class Question:

    a = '11593'
    b = '23453'
    c = '57784'

    def __init__(self, question_id, quiz_id, question, a_one, a_two, a_three, good, img_url=None):
        """
        :param question_id: int (id from DB)
        :param quiz_id: int (quiz_id for which question is
        :param question: string (text of question)
        :param a_one: string (text of first answer)
        :param a_two: string (text of second answer)
        :param a_three: string (text of third answer)
        :param good: string (text of good answer)
        :param img_url: string (url to img if given)
        """
        self.question_id = question_id
        self.quiz_id = quiz_id
        self.question = question
        self.a_one = a_one
        self.a_two =a_two
        self.a_three = a_three
        self.good = good
        self.img_url = img_url


    # @classmethod
    # def add_question(cls, quiz_id, question, a_one, a_two, a_three, good, img_url=None):
    #     """"""
    #     query = "SELECT max(ID) FROM QUESTIONS"
    #     new_id = sql.query(query)[0][0] + 1
    #     new_question = cls(new_id, quiz_id, question, a_one, a_two, a_three, good, img_url)
    #     query_2 = """INSERT INTO QUESTIONS (quiz_id, question, a_one, a_two, a_three, a_good, img)
    #                  VALUES (?, ?, ?, ?, ?, ?, ?)"""
    #     params = [quiz_id, question, a_one, a_two, a_three, good, img_url]
    #     sql.query(query_2, params)
    #     return new_question

    @classmethod
    def if_answer_correct(cls, user_choice, quizId, answerId):
        query = "SELECT a_good FROM QUESTIONS WHERE quiz_id=(?) AND `number`=(?)"
        params = [quizId, answerId]
        good_answer = sql.query(query, params)[0][0]

        if user_choice == cls.a:
            user_choice = 'a'
        elif user_choice == cls.b:
            user_choice = 'b'
        elif user_choice == cls.c:
            user_choice = 'c'

        if user_choice == good_answer:
            return True
        return False

    @staticmethod
    def get_questions_by_id(quiz_id):
        query = "SELECT * FROM QUESTIONS WHERE quiz_id=(?)"
        ans_list = sql.query(query, [quiz_id])
        list_to_push =[]
        for ans in ans_list:
            list_to_push.append([ans['id'], ans['number'], ans['quiz_id'], ans['img'], ans['question'], ans['a_one'], ans['a_two'], ans['a_three'],
                                 ans['a_good']])
        return list_to_push

    @staticmethod
    def check_answers(lista_punktow):
        query_2 = 'DROP TABLE `answers`;'
        new_id = sql.query(query_2)
        query = "CREATE TABLE `answers` (`ID` INTEGER, `username` TEXT NOT NULL,  `socket`, `time` TEXT NOT NULL, PRIMARY KEY(`ID`));"
        new_id = sql.query(query)
        for socket in lista_punktow:
            query_3 = """INSERT INTO `answers` (`username`, `socket`, `time`)
                                   VALUES (?, ?, ?)"""
            params = socket
            new_id = sql.query(query_3, params)

        # query = """SELECT  username, count(username) FROM answers GROUP BY username;"""



        # query_2 =
        # new_question = cls(new_id, quiz_id, question, a_one, a_two, a_three, good, img_url)
        # query_2 = """INSERT INTO QUESTIONS (quiz_id, question, a_one, a_two, a_three, a_good, img)
        #                      VALUES (?, ?, ?, ?, ?, ?, ?)"""




    def __str__(self):
        return '{}-{}-{}'.format(self.question_id, self.question, self.good)

"""question = 'Who is this?'
a_one = 'Pope'
a_two = 'Santa'
a_three = 'Pikachu'
good = 'Pikachu'
img = "http://cartoonbros.com/wp-content/uploads/2016/08/pikachu-6.png"
print(Question.add_question(3, question, a_one, a_two, a_three, good, img))
Question.get_questions_by_id(1)"""
print(Question.if_answer_correct('23453', 1, 1))