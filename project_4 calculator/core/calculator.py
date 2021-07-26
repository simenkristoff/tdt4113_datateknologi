"""Calculator module"""
import numbers
import re

import numpy

from project_4.containers.queue import Queue
from project_4.containers.stack import Stack
from project_4.core.function import Function
from project_4.core.operator_helper import Operator


class Calculator:
    """Class calculator"""

    def __init__(self):
        """
        Initialize the calculator's functions and operators
        """

        # Define the supported functions
        self.functions = {'EXP': Function(numpy.exp),
                          'LOG': Function(numpy.log),
                          'SIN': Function(numpy.sin),
                          'SINE': Function(numpy.sin),
                          'COS': Function(numpy.cos),
                          'COSINE': Function(numpy.cos),
                          'SQRT': Function(numpy.sqrt)}

        # Define the supported operators
        self.operators = {'ADD': Operator(numpy.add, 0),
                          'PLUS': Operator(numpy.add, 0),
                          'SUBTRACT': Operator(numpy.subtract, 0),
                          'MINUS': Operator(numpy.subtract, 0),
                          'MULTIPLY': Operator(numpy.multiply, 1),
                          'TIMES': Operator(numpy.multiply, 1),
                          'DIVIDE': Operator(numpy.divide, 1)}

        # Define the output queue
        self.output_queue = Queue()

    def evaluate_rpn(self):
        """
        Evaluate the the output queue with use of reverse polish notation
        :return: the calculated result
        """
        stack = Stack()
        while not self.output_queue.is_empty():
            _e = self.output_queue.pop()
            if isinstance(_e, numbers.Number):
                stack.push(_e)
            elif isinstance(_e, Function):
                stack.push(_e.execute(stack.pop(), debug=False))
            else:
                _r, _l = stack.pop(), stack.pop()
                stack.push(_e.execute(_l, _r))
        return stack.pop()

    def shunting_yard(self, queue: Queue):
        """
        Builds a RPN queue by using the shunting yard algorithm. This algorithm
        assumes that each element in the queue is either a number, operation,
        function, or a left/right parenthesis.
        """
        stack = Stack()
        while not queue.is_empty():
            ele = queue.pop()
            if isinstance(ele, numbers.Number):
                self.output_queue.push(ele)
            elif isinstance(ele, Function):
                stack.push(ele)
            elif ele == '(':
                stack.push(ele)
            elif ele == ')':
                while True and not stack.is_empty():
                    item = stack.pop()
                    if item != '(':
                        self.output_queue.push(item)
                        continue
                    break
            else:
                while True and not stack.is_empty():
                    item = stack.peek()

                    if (isinstance(item,
                                   Operator) and ele > item) or item == '(':
                        break
                    self.output_queue.push(stack.pop())

                stack.push(ele)

        while not stack.is_empty():
            self.output_queue.push(stack.pop())

    def parse_text(self, query: str):
        """
        Pre-process math queries before running the shunting yard algorithm
        :param query: the math query
        :return: queue of mathematical objects
        """

        queue = Queue()
        query = query.replace(" ", "").upper()

        operators_pattern = "|".join(["^" + func for func in self.operators])
        functions_pattern = "|".join(["^" + func for func in self.functions])
        numbers_pattern = r"^[-0123456789.]+"

        while True and query:
            if query.startswith("("):
                queue.push('(')
                query = query[1:]
            elif query.startswith(")"):
                queue.push(')')
                query = query[1:]
            elif match := re.search(operators_pattern, query):
                queue.push(self.operators[match.group(0)])
                query = query.replace(match.group(0), "", 1)
            elif match := re.search(functions_pattern, query):
                queue.push(self.functions[match.group(0)])
                query = query.replace(match.group(0), "", 1)
            elif match := re.search(numbers_pattern, query):
                num = match.group(0)
                queue.push(float(num) if '.' in num else int(num))
                query = query.replace(num, "", 1)
            else:
                raise TypeError("Invalid argument type")

        return queue

    def start(self):
        """
        Starts the calculator instance
        :return:
        """
        while True:
            self.output_queue.clear()
            query = input("Enter expression: ")
            try:
                self.shunting_yard(self.parse_text(query))
                print(f"{query} = {self.evaluate_rpn()}")
            except (TypeError, AssertionError, ValueError):
                print("Error -> Invalid expression, try again")
