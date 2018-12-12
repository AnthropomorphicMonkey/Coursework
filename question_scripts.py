class Question:
    def __init__(self, difficulty: int):
        self.difficulty = ()
        self.set_difficulty(difficulty)
        self.question_text = ()
        self.correct_answer = ()
        self.answer_b = ()
        self.answer_c = ()
        self.answer_d = ()
        self.type_id = ()

    def set_difficulty(self, difficulty: int):
        self.difficulty = difficulty

    def set_question(self, question: str):
        self.question_text = question

    def set_correct_answer(self, answer: str):
        self.correct_answer = answer

    def set_answer_b(self, answer: str):
        self.answer_b = answer

    def set_answer_c(self, answer: str):
        self.answer_c = answer

    def set_answer_d(self, answer: str):
        self.answer_d = answer

    def set_type_id(self, type_id: int):
        self.type_id = type_id

    def get_database_values(self) -> tuple:
        return self.question_text, self.correct_answer, self.answer_b, self.answer_c, self.answer_d


if __name__ == '__main__':
    pass
