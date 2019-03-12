import sympy
import math
import random


def generate_polynomial(order: int):
    if order < 0:
        raise ValueError
    x = sympy.symbols('x')
    function = random.randint(0, 100) * x ** order
    for exponent in range(0, order):
        function += random.randint(0, 4) * x ** exponent
    return function


def generate_compound_trig_function(complexity: int):
    if complexity < 1:
        raise ValueError
    x = sympy.symbols('x')
    trig_functions = (sympy.sin(x), sympy.cos(x), sympy.tan(x), sympy.sec(x), sympy.csc(x), sympy.cot(x))
    function = random.randint(1, 100)
    for extra_functions in range(complexity):
        function *= random.choice(trig_functions)
    return function


if __name__ == '__main__':
    x = sympy.symbols('x')
    fn = generate_polynomial(7)
    print(fn)
    print(fn.subs(x, 9))
    fn = generate_compound_trig_function(4)
    print(fn)
    print(float(fn.subs(x, 9)))
