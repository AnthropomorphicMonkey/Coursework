import sympy


class IntegralApproximationBase:
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        # Errors if invalid number of strips entered
        if number_of_strips < 1:
            raise Exception('Number of strips must be greater than 0')
        # Stores all constant values related to the range within which the integral is to be calculated, what function
        # is being integrated and how many strips are to be used (accuracy level of approximation)
        self.number_of_strips: int = number_of_strips
        self.upper_limit: float = upper_limit
        self.lower_limit: float = lower_limit
        self.function = function
        # Calculates strip width as the range of the integral divided by the desired number of strips
        self.strip_width: float = (upper_limit - lower_limit) / number_of_strips
        # Finds and stores the y values at the boundary between each strip
        self.y_list: list = self.get_y_values()

    def get_y_values(self) -> list:
        # Variable to keep track of number of y values calculated
        y_counter: int = 0
        # List to store all y values
        y_values: list = []
        # Until each y value has been found, calculates the y for value for each x value from the lower limit to the
        # upper limit at intervals of the strip width and stores within the y_values attribute
        while y_counter <= self.number_of_strips:
            x_value: float = self.lower_limit + (self.strip_width * y_counter)
            x = sympy.symbols('x')
            y_values.append(self.function.subs(x, x_value))
            y_counter += 1
        # Returns list of y values
        return y_values


class TrapeziumRule(IntegralApproximationBase):
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        # Initialises child class with no changes to parent class
        super().__init__(number_of_strips, upper_limit, lower_limit, function)

    def integral(self):
        # Approximates integral using equation defined in design. Y sum stores the sum of all the y values, with all
        # but the first and last being added twice as they are both the end of one trapezium and start of the next
        y_sum: float = self.y_list[0] + self.y_list[-1]
        counter: int = 1
        for y in self.y_list[1:-1]:
            y_sum += y * 2
            counter += 1
        # Multiplies y sum by half the strip width to get the approximate integral and returns the value
        return float((self.strip_width / 2) * y_sum)


class SimpsonsRule(IntegralApproximationBase):
    def __init__(self, number_of_strips: int, upper_limit: float, lower_limit: float, function):
        # Verifies that strip count is even as required(see design) and errors if not (validation should occur before
        # using class), then initialises class identically to parent class
        if number_of_strips % 2 != 0:
            raise Exception('Number of strips must be even')
        super().__init__(number_of_strips, upper_limit, lower_limit, function)

    def integral(self):
        # Approximates integral using equation defined in design. y sum stores the sum of all y values, with the first
        # and last value being added once, and all other values from the second y value through to the penultimate
        # alternating between being added four times and twice respectively
        y_sum: float = self.y_list[0] + self.y_list[-1]
        counter: int = 1
        for y in self.y_list[1:-1]:
            if counter % 2 == 0:
                y_sum += y * 2
            else:
                y_sum += y * 4
            counter += 1
        # Multiplies y sum by 1/3 the strip width to get the approximate integral and returns the value
        return float((self.strip_width / 3) * y_sum)


class DefiniteIntegral(SimpsonsRule):
    def __init__(self, upper_limit: float, lower_limit: float, function):
        number_of_strips: int = 100
        super().__init__(number_of_strips, upper_limit, lower_limit, function)
