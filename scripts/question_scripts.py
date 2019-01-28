import random
import math
import sqlite3

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


class Question:
    def __init__(self, name: str, type_id: int, difficulty: int, question_text: str, correct_answer, **kwargs: str):
        # Difficulty should be greater than or equal to 1, this should be verified before using function
        self.name: str = name
        self.type_id: int = type_id
        self.difficulty: int = difficulty
        self.question_text: str = question_text
        self.correct_answer: str = correct_answer
        self.answer_b: str = ()
        self.answer_c: str = ()
        self.answer_d: str = ()
        try:
            self.correct_answer: float = float(self.correct_answer)
            self.set_incorrect_numerical_answers()
        except ValueError:
            self.set_incorrect_answers("N/A", "N/A", "N/A")
        if 'answer_b' in kwargs:
            self.answer_b: str = kwargs.get('answer_b')
        if 'answer_c' in kwargs:
            self.answer_c: str = kwargs.get('answer_c')
        if 'answer_d' in kwargs:
            self.answer_d: str = kwargs.get('answer_d')

    def set_incorrect_answers(self, answer_b, answer_c, answer_d):
        self.answer_b: str = answer_b
        self.answer_c: str = answer_c
        self.answer_d: str = answer_d

    def set_incorrect_numerical_answers(self):
        significant_figures: int = len(str(self.correct_answer).replace('.', ''))
        answer_b: float = self.correct_answer
        answer_c: float = self.correct_answer
        answer_d: float = self.correct_answer
        while answer_b == self.correct_answer:
            answer_b: float = self.round_value(self.generate_incorrect_numerical_value(), significant_figures)
        while answer_c in [self.correct_answer, answer_b]:
            answer_c: float = self.round_value(self.generate_incorrect_numerical_value(), significant_figures)
        while answer_d in [self.correct_answer, answer_b, answer_c]:
            answer_d: float = self.round_value(self.generate_incorrect_numerical_value(), significant_figures)
        self.set_incorrect_answers(answer_b, answer_c, answer_d)

    def generate_incorrect_numerical_value(self) -> float:
        incorrect_answer: float = random.uniform((self.correct_answer - (self.correct_answer * (1 / self.difficulty))),
                                                 (self.correct_answer + (self.correct_answer * (1 / self.difficulty))))
        return incorrect_answer

    @staticmethod
    def round_value(value, significant_figures) -> float:
        # https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
        return round(value, significant_figures - int(math.floor(math.log10(abs(value)))) - 1)


def save_question(question):
    sql: str = 'INSERT INTO questions(name, type_id, question_text, correct_answer, answer_b, answer_c, answer_d)' \
               'VALUES(?, ?, ?, ?, ?, ?, ?);'
    c.execute(sql, (question.name, question.type_id, question.question_text, question.correct_answer, question.answer_b,
                    question.answer_c, question.answer_d))
    conn.commit()


if __name__ == '__main__':
    test_question = Question("Question", 1, 1, "Correct answer is 5.87", 5.87, answer_b="Hello")
    print("Difficulty:", test_question.difficulty)
    print("Question:", test_question.question_text)
    print("Correct answer:", test_question.correct_answer)
    print("Answer B:", test_question.answer_b)
    print("Answer C:", test_question.answer_c)
    print("Answer D:", test_question.answer_d)
    test_question = Question("Question", 1, 1, "Correct answer is qwerty", "qwerty", answer_c="Hello")
    print("Difficulty:", test_question.difficulty)
    print("Question:", test_question.question_text)
    print("Correct answer:", test_question.correct_answer)
    print("Answer B:", test_question.answer_b)
    print("Answer C:", test_question.answer_c)
    print("Answer D:", test_question.answer_d)
    test_question = Question("Question", 1, 100, "Correct answer is 5.87", "5.8734", answer_d="Hello")
    print("Difficulty:", test_question.difficulty)
    print("Question:", test_question.question_text)
    print("Correct answer:", test_question.correct_answer)
    print("Answer B:", test_question.answer_b)
    print("Answer C:", test_question.answer_c)
    print("Answer D:", test_question.answer_d)
    save_question(test_question)
