import random
import math
import sqlite3

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


class Question:
    def __init__(self, name: str, type_id: int, difficulty: int, question_text: str, correct_answer, answer_b=None,
                 answer_c=None, answer_d=None):
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
        if answer_b is not None:
            self.answer_b: str = answer_b
        if answer_c is not None:
            self.answer_c: str = answer_c
        if answer_d is not None:
            self.answer_d: str = answer_d

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

    def save_question(self) -> int:
        sql: str = 'INSERT INTO questions(name, type_id, question_text, correct_answer, answer_b, answer_c, answer_d)' \
                   'VALUES(?, ?, ?, ?, ?, ?, ?);'
        c.execute(sql, (self.name, self.type_id, self.question_text, self.correct_answer, self.answer_b,
                        self.answer_c, self.answer_d))
        sql: str = 'SELECT last_insert_rowid()'
        c.execute(sql)
        inserted_position: int = c.fetchall()[0][0]
        conn.commit()
        return inserted_position


if __name__ == '__main__':
    pass
