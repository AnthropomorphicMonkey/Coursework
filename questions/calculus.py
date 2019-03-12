import questions.question_scripts as question_scripts
import maths_scripts.calculus
import maths_scripts.general
import random


def simpsons_rule(difficulty: int) -> question_scripts.Question:
    type_id = 2
    number_of_strips = random.choice([4, 6, 8])
    upper_limit = random.randint(3, 10)
    lower_limit = random.randint(1, upper_limit - 1)
    function_type = random.choice([1, 2])
    if function_type == 1 or difficulty < 3:
        function = maths_scripts.general.generate_polynomial(random.randint(0, difficulty))
    elif function_type == 2 and difficulty >= 3:
        function = maths_scripts.general.generate_compound_trig_function(random.randint(1, difficulty))
    else:
        raise ValueError
    simpsons_rule_instance = maths_scripts.calculus.SimpsonsRule(number_of_strips, upper_limit, lower_limit, function)
    question_text = "Approximate ∫ {} dx using Simpson's Rule with {} strips " \
                    "between x = {} and x = {}".format(function, number_of_strips, lower_limit, upper_limit)
    correct_answer = round(simpsons_rule_instance.integral(), 2)
    question = question_scripts.Question("Simpson's Rule", type_id, difficulty, question_text, correct_answer)
    return question


def trapezium_rule(difficulty: int) -> question_scripts.Question:
    type_id = 3
    number_of_strips = random.randint(4, 8)
    upper_limit = random.randint(3, 10)
    lower_limit = random.randint(1, upper_limit - 1)
    function_type = random.choice([1, 2])
    if function_type == 1 or difficulty < 3:
        function = maths_scripts.general.generate_polynomial(random.randint(0, difficulty))
    elif function_type == 2 and difficulty >= 3:
        function = maths_scripts.general.generate_compound_trig_function(random.randint(1, difficulty))
    else:
        raise ValueError
    trapezium_rule_instance = maths_scripts.calculus.TrapeziumRule(number_of_strips, upper_limit, lower_limit, function)
    question_text = "Approximate ∫ {} dx using the Trapezium Rule with {} strips " \
                    "between x = {} and x = {}".format(function, number_of_strips, lower_limit, upper_limit)
    correct_answer = round(trapezium_rule_instance.integral(), 2)
    question = question_scripts.Question("Trapezium Rule", type_id, difficulty, question_text, correct_answer)
    return question


if __name__ == '__main__':
    q: question_scripts.Question = simpsons_rule(4)
    print(q.question_text)
    print(q.correct_answer)
    print(q.answer_b)
    print(q.answer_c)
    print(q.answer_d)
