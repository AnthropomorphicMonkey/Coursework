import sympy
import math


class SimpsonsRule:
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        self.number_of_strips: int = number_of_strips
        if number_of_strips % 2 != 0:
            raise ValueError
        self.h: float = (upper_limit - lower_limit) / number_of_strips
        self.upper_limit: float = upper_limit
        self.lower_limit: float = lower_limit
        self.function = function
        self.y_list: list = []
        self.get_y_values()

    def get_y_values(self):
        x_value: float = self.lower_limit
        while x_value <= self.upper_limit:
            x = sympy.symbols('x')
            self.y_list.append(self.function.subs(x, x_value))
            x_value += self.h

    def integral(self):
        y_sum: float = 0
        counter: int = 1
        for y in self.y_list:
            if counter % 3 == 0:
                y_sum += y * 2
            elif counter % 2 == 0:
                y_sum += y * 4
            else:
                y_sum += y
            counter += 1
        return (self.h / 3) * y_sum


if __name__ == '__main__':
    x = sympy.symbols('x')
    fn = x ** (3 / 2)
    simpson = SimpsonsRule(4, 6, 2, fn)
    print(simpson.integral())
