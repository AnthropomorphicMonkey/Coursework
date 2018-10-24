import sympy

x, y, z = sympy.symbols('x y z')
sympy.init_printing(use_unicode=True)
print(sympy.diff(x**2), x)
