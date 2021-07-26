"""Function module"""
import numbers


class Function:
    """Class Function"""

    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=True):
        """
        Executes the function on an element of number type
        :param element: the function element/number
        :param debug: print function to console or not
        :return: the calculated results
        """

        # Check type
        if not isinstance(element, numbers.Number):
            raise TypeError("The element must be a number")
        result = self.func(element)

        # Debug
        if debug is True:
            print(f"Function: {self.func.__name__}({element}) = {result}")
        return result

    def __str__(self):
        """
        Represent the function in string format.
        :return: Function as string
        """
        return self.func.__name__
