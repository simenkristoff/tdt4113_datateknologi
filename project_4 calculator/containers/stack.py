"""Stack module"""
from project_4.containers.container import Container


class Stack(Container):
    """Class Stack"""
    def peek(self):
        """
        Return top element in the stack without removing it
        :return: top element of the stack
        """
        return self._items[-1]

    def pop(self):
        """
        Pop the top element in the stack
        :return: top element of the stack
        """
        assert not self.is_empty()
        return self._items.pop()
