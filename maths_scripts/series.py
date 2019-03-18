import sympy
import maths_scripts


class Taylor:
    def __init__(self, function: sympy.add.Add, centre: int):
        x = sympy.symbols('x')
        self.function = function
        self.centre = centre
        if function.subs(x, self.centre) == sympy.zoo:
            raise Exception("Invalid centre")

    def equation_in_x(self, precision: int) -> sympy.add.Add:
        x = sympy.symbols('x')
        final_equation: sympy.add.Add = 0
        function: sympy.add.Add = self.function
        for n in range(0, precision):
            f: float = function.subs(x, self.centre)
            final_equation += (f / maths_scripts.integer_factorial(n)) * ((x - self.centre) ** n)
            function = sympy.diff(function, x)
        return final_equation

    def evaluate(self, value: float, precision: int) -> float:
        x = sympy.symbols('x')
        function = self.equation_in_x(precision)
        return function.subs(x, value)


class Maclaurin(Taylor):
    def __init__(self, function: sympy.add.Add):
        super().__init__(function, 0)


if __name__ == '__main__':
    x1: sympy.add.Add = sympy.symbols('x')
    function1 = sympy.ln(8)
    centre1: int = 6
    precision1: int = 100
    value1: float = 1
    series: Taylor = Taylor(function1, centre1)
    print(series.equation_in_x(precision1))
    print(float(series.evaluate(value1, precision1)))
    series: Maclaurin = Maclaurin(function1)
    print(series.equation_in_x(precision1))
    print(float(series.evaluate(value1, precision1)))
