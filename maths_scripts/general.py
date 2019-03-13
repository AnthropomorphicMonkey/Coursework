import random

import sympy


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


def check_divergent(upper_limit: float, lower_limit: float, function) -> bool:
    if lower_limit > upper_limit:
        raise Exception("Upper limit must be greater or equal")
    x = sympy.symbols('x')
    check_position = sympy.ceiling(lower_limit / (sympy.pi / 2))
    if str(sympy.tan(x)) in str(function) or str(sympy.sec(x)) in str(function):
        if check_position % 2 == 0:
            check_position += 1
    elif str(sympy.cot(x)) in str(function) or str(sympy.csc(x)) in str(function):
        if check_position % 2 != 0:
            check_position += 2
    else:
        return False
    if (check_position * (sympy.pi / 2)) <= upper_limit:
        return True
    else:
        return False



if __name__ == '__main__':
    x = sympy.symbols('x')
    fn = 30*x**4 + x**3 + 4*x
    upper_limit = 0 * (sympy.pi / 2)
    lower_limit = upper_limit
    print(check_divergent(upper_limit, lower_limit, fn))
    upper_limit = 1 * (sympy.pi / 2)
    lower_limit = upper_limit
    print(check_divergent(upper_limit, lower_limit, fn))
    upper_limit = 2 * (sympy.pi / 2)
    lower_limit = upper_limit
    print(check_divergent(upper_limit, lower_limit, fn))
    upper_limit = 3 * (sympy.pi / 2)
    lower_limit = upper_limit
    print(check_divergent(upper_limit, lower_limit, fn))
    upper_limit = 4 * (sympy.pi / 2)
    lower_limit = upper_limit
    print(check_divergent(upper_limit, lower_limit, fn))
