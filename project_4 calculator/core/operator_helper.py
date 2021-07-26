"""Operator module"""
import numbers


class Operator:
    """Class operator"""

    def __init__(self, operator, strength):
        self._operator = operator
        self.strength = strength

    def get_strength(self):
        """
        Gets the strength of the operator
        :return: the strength of the operator
        """

        return self.strength

    def execute(self, first_element, second_element, debug=True):
        """
        Executes the operator

        :param first_element: the first element in the operation
        :param second_element: the second element in the operation
        :param debug: print function to console or not
        :return: the calculated results
        """

        # Check type
        if not isinstance(first_element, numbers.Number) or not isinstance(
                second_element, numbers.Number):
            raise TypeError("The element must be a number")
        result = self._operator(first_element, second_element)

        # Debug
        if debug is True:
            print(f"Operation: {first_element} {self._operator.__name__} "
                  + f"{second_element} = {result}")

        return result

    def __gt__(self, element):
        """
        Check if this object has greater strength than other object
        :param element: the element to check against
        :return:
        """

        return self.strength > element.strength
