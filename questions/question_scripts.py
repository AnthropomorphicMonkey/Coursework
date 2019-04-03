import random
import sqlite3

# Connects to database
conn = sqlite3.connect('database.db')
c = conn.cursor()


class Question:
    def __init__(self, name: str, type_id: int, difficulty: int, question_text: str, correct_answer, answer_b=None,
                 answer_c=None, answer_d=None):
        # Difficulty should be greater than or equal to 1, this should be verified before using function
        if difficulty < 1:
            raise ValueError
        self.name: str = name
        self.type_id: int = type_id
        self.difficulty: int = difficulty
        self.question_text: str = question_text
        self.correct_answer: str = correct_answer
        self.answer_b: str = ""
        self.answer_c: str = ""
        self.answer_d: str = ""
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
        answer_b: float = self.correct_answer
        answer_c: float = self.correct_answer
        answer_d: float = self.correct_answer
        decimal_places = get_decimal_place_count(self.correct_answer)
        while answer_b == self.correct_answer:
            answer_b: float = round(self.generate_incorrect_numerical_value(), decimal_places)
            answer_b: str = round_to_decimal_places_as_string(answer_b, decimal_places)
        while answer_c in [self.correct_answer, answer_b]:
            answer_c: float = round(self.generate_incorrect_numerical_value(), decimal_places)
            answer_c: str = round_to_decimal_places_as_string(answer_c, decimal_places)
        while answer_d in [self.correct_answer, answer_b, answer_c]:
            answer_d: float = round(self.generate_incorrect_numerical_value(), decimal_places)
            answer_d: str = round_to_decimal_places_as_string(answer_d, decimal_places)
        self.set_incorrect_answers(answer_b, answer_c, answer_d)

    def generate_incorrect_numerical_value(self) -> float:
        if round(self.correct_answer, 1) == 0:
            incorrect_answer: float = random.uniform((self.correct_answer - (2 * (1 / self.difficulty))),
                                                     (self.correct_answer + (2 * (1 / self.difficulty))))
        else:
            incorrect_answer: float = random.uniform(
                (self.correct_answer - (self.correct_answer * (1 / self.difficulty))),
                (self.correct_answer + (self.correct_answer * (1 / self.difficulty))))
        return incorrect_answer

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


def get_decimal_place_count(value: float) -> int:
    decimal_position: int = str(value).find('.') + 1
    return len(str(value)[decimal_position:])


def round_to_decimal_places_as_string(value: float, decimal_places: int) -> str:
    rounded_value: float = round(value, decimal_places)
    rounded_value: str = str(rounded_value) + '0' * (decimal_places - get_decimal_place_count(rounded_value))
    return str(rounded_value)

