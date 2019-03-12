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
        y_counter = 0
        while y_counter <= self.number_of_strips:
            x_value: float = self.lower_limit + (self.h * y_counter)
            x = sympy.symbols('x')
            self.y_list.append(self.function.subs(x, x_value))
            y_counter += 1

    def integral(self):
        y_sum: float = self.y_list[0] + self.y_list[-1]
        counter: int = 1
        for y in self.y_list[1:-1]:
            if counter % 2 == 0:
                y_sum += y * 2
            else:
                y_sum += y * 4
            counter += 1
        return float((self.h / 3) * y_sum)


if __name__ == '__main__':
    x = sympy.symbols('x')
    fn = 57*sympy.cosh(x)*sympy.tan(x)**2
    print("∫", fn, "dx between x = 0 and x = 1")
    strips = 2
    while True:
        simpson = SimpsonsRule(strips, 1, 0, fn)
        print(strips)
        print(simpson.integral())
        strips += 2
