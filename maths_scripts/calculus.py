import sympy
import random
from questions import question_scripts


def generate_polynomial(max_exponent):
    return x ** 2


class DifferentiationQuestion(question_scripts.Question):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.equation = ()
        self.generate_equation()

    def generate_equation(self):
        self.equation = generate_polynomial(self.difficulty)

    def generate_question(self):
        self.question_text = "Find the".format()

    def derivative(self):
        return sympy.diff(self.equation)


class EvaluatedDifferentiationQuestion(DifferentiationQuestion):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.value = ()
        self.generate_value()

    def generate_value(self):
        self.value = random.randint(-self.difficulty * 100, self.difficulty * 100)


if __name__ == '__main__':
    pass
