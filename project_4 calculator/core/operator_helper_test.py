"""Test Function Module"""
import numpy

from project_4.core.operator_helper import Operator

# Add operation
add_op = Operator(numpy.add, 0)
assert add_op.execute(2, 123) == 125

# Subtract operation
sub_op = Operator(numpy.subtract, 0)
assert sub_op.execute(10, 20) == -10

# Multiply operation
mul_op = Operator(numpy.multiply, 1)
assert mul_op.execute(5, 5) == 25

# Divide operation
div_op = Operator(numpy.divide, 1)
assert round(div_op.execute(9, 6), 2) == 1.50
