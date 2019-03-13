import sympy


class IntegralApproximationBase:
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        self.number_of_strips: int = number_of_strips
        self.strip_width: float = (upper_limit - lower_limit) / number_of_strips
        self.upper_limit: float = upper_limit
        self.lower_limit: float = lower_limit
        self.function = function
        self.y_list: list = []
        self.get_y_values()

    def get_y_values(self):
        y_counter = 0
        while y_counter <= self.number_of_strips:
            x_value: float = self.lower_limit + (self.strip_width * y_counter)
            x = sympy.symbols('x')
            self.y_list.append(self.function.subs(x, x_value))
            y_counter += 1


class TrapeziumRule(IntegralApproximationBase):
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        if number_of_strips < 1:
            raise Exception('Number of strips must be greater than 0')
        super().__init__(number_of_strips, upper_limit, lower_limit, function)

    def integral(self):
        y_sum: float = self.y_list[0] + self.y_list[-1]
        counter: int = 1
        for y in self.y_list[1:-1]:
            y_sum += y * 2
            counter += 1
        return float((self.strip_width / 2) * y_sum)


class SimpsonsRule(IntegralApproximationBase):
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        if number_of_strips % 2 != 0:
            raise Exception('Number of strips must be even')
        super().__init__(number_of_strips, upper_limit, lower_limit, function)

    def integral(self):
        y_sum: float = self.y_list[0] + self.y_list[-1]
        counter: int = 1
        for y in self.y_list[1:-1]:
            if counter % 2 == 0:
                y_sum += y * 2
            else:
                y_sum += y * 4
            counter += 1
        return float((self.strip_width / 3) * y_sum)


if __name__ == '__main__':
    x = sympy.symbols('x')
    fn = 100 * x + 1
    print("∫", fn, "dx between x = 0 and x = 1")
    strips = 2
    trapezium = TrapeziumRule(strips, 7, 6, fn)
    print(trapezium.integral())
    simpson = SimpsonsRule(strips, 7, 6, fn)
    print(simpson.integral())
