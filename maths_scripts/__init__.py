import random
import sympy
import maths_scripts.series as series

pi = 3.141592653589793


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
    check_position = sympy.ceiling(lower_limit / (pi / 2))
    if str(sympy.tan(x)) in str(function) or str(sympy.sec(x)) in str(function):
        if check_position % 2 == 0:
            check_position += 1
    elif str(sympy.cot(x)) in str(function) or str(sympy.csc(x)) in str(function):
        if check_position % 2 != 0:
            check_position += 2
    else:
        return False
    if (check_position * (pi / 2)) <= upper_limit:
        return True
    else:
        return False


def integer_factorial(number: int) -> int:
    if number == 0:
        return 1
    else:
        final_value: int = 1
        for i in range(1, number + 1):
            final_value: int = final_value * i
        return final_value


def sin(value: float) -> float:
    precision = 100
    x = sympy.symbols('x')
    if value > 0:
        value -= 2 * pi * (value // (2 * pi))
    else:
        value += 2 * pi * (value // (-2 * pi))
    final_equation: sympy.add.Add = 0
    for n in range(0, precision):
        final_equation += (-1) ** n / integer_factorial(2 * n + 1) * (x ** (2 * n + 1))
    return final_equation.subs(x, value)


def cos(value: float) -> float:
    precision = 100
    x = sympy.symbols('x')
    if value > 0:
        value -= 2 * pi * (value // (2 * pi))
    else:
        value += 2 * pi * (value // (-2 * pi))
    final_equation: sympy.add.Add = 1
    for n in range(0, precision - 1):
        final_equation += (-1) ** (n + 1) / integer_factorial(2 * (n + 1)) * (x ** (2 * (n + 1)))
    return final_equation.subs(x, value)


def tan(value: float) -> float:
    return sin(value) / cos(value)


if __name__ == '__main__':
    print(sin(-5))
    print(cos(-5))
    print(tan(5))
    x1 = sympy.symbols('x')
    fn = 30 * x1 ** 4 + x1 ** 3 + 4 * x1
    upper = 0 * (pi / 2)
    lower = upper
    print(check_divergent(upper, lower, fn))
    upper = 1 * (pi / 2)
    lower = upper
    print(check_divergent(upper, lower, fn))
    upper = 2 * (pi / 2)
    lower = upper
    print(check_divergent(upper, lower, fn))
    upper = 3 * (pi / 2)
    lower = upper
    print(check_divergent(upper, lower, fn))
    upper = 4 * (pi / 2)
    lower = upper
    print(check_divergent(upper, lower, fn))
