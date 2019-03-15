import sympy

x = sympy.symbols('x')

function = sympy.sympify('csc(x)')
print(float(function.subs(x, 109)))
question = "test"
print(question, None, None, None)
