"""Test Calculator module"""
from project_4.core.calculator import Calculator

calc = Calculator()

# Test basic calculator
assert round(calc.functions['EXP']
             .execute(calc.operators['ADD']
                      .execute(1, calc.operators['MULTIPLY']
                               .execute(2, 3))), 2) == 1096.63

# Test RPN evaluation
calc.output_queue.push(1)
calc.output_queue.push(2)
calc.output_queue.push(3)
calc.output_queue.push(calc.operators['MULTIPLY'])
calc.output_queue.push(calc.operators['ADD'])
calc.output_queue.push(calc.functions['EXP'])
assert round(calc.evaluate_rpn(), 2) == 1096.63
