"""Test Function Module"""
import numpy

from project_4.core.function import Function

# Exponential function
exp_func = Function(numpy.exp)
assert round(exp_func.execute(2), 2) == 7.39

# Logarithmic function
log_func = Function(numpy.log)
assert round(log_func.execute(10), 2) == 2.30

# Sin function
sin_func = Function(numpy.sin)
assert round(sin_func.execute(0.5 * 3.14), 2) == 1.00

# Cos function
cos_func = Function(numpy.cos)
assert round(cos_func.execute(0), 2) == 1.00

# Square root function
sqrt_func = Function(numpy.sqrt)
assert sqrt_func.execute(49) == 7
