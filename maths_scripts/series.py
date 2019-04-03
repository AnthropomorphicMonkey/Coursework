import sympy
import maths_scripts


# Class to generate a taylor series and approximate values fora given function and centre
class Taylor:
    def __init__(self, function: sympy.add.Add, centre: int):
        # Sets up x as a variable in SymPy
        x = sympy.symbols('x')
        # Defines constants containing the function to be expanded and the centre
        self.function = function
        self.centre = centre
        # Outputs an error if a function is entered with an invalid centre (function is undefined at centre)
        if function.subs(x, self.centre) == sympy.zoo:
            raise Exception("Invalid centre")

    def equation_in_x(self, precision: int) -> sympy.add.Add:
        # Sets up x as a variable in SymPy
        x = sympy.symbols('x')
        # Initialises variable to hold final function as nothing
        final_equation: sympy.add.Add = sympy.add.Add(0)
        # Initialises variable to hold the next derivative to be used during expansion as the value of the initial
        # function
        function: sympy.add.Add = self.function
        # Loops through for the number of terms entered as the precision and generates next term in the Taylor series
        # on each loop
        for n in range(0, precision):
            # Calculates the value of the current function at the centre of expansion
            f: float = function.subs(x, self.centre)
            # Uses formula (see design section) to generate the next term in x in the Taylor series and add to end of
            # current full expansion
            final_equation += (f / maths_scripts.integer_factorial(n)) * ((x - self.centre) ** n)
            # Replaces current function with the derivative of the current function
            function = sympy.diff(function, x)
        # Returns full expansion up to number of terms specified
        return final_equation

    def evaluate(self, value: float, precision: int) -> float:
        # Sets up x as a variable in SymPy
        x = sympy.symbols('x')
        # Generates Taylor series to given precision and substitutes value of x with given value to evaluate function
        function = self.equation_in_x(precision)
        # Returns final value
        return function.subs(x, value)


class Maclaurin(Taylor):
    def __init__(self, function: sympy.add.Add):
        # Inherits all code from Taylor series class while as Maclaurin series is simply a special case of it with
        # centre of expansion 0. Centre of expansion is therefore not required to be passed when declaring instance of
        # class as it can always be passed to parent class as 0
        super().__init__(function, 0)

