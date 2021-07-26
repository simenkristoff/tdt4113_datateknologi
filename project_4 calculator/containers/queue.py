"""Queue module"""
from containers.container import Container


class Queue(Container):
    """Class Queue"""

    def peek(self):
        """
        Return top element in the queue without removing it
        :return: top element of the queue
        """
        return self._items[0]

    def pop(self):
        """
        Pop the top element in the queue
        :return: top element of the queue
        """
        assert not self.is_empty()
        return self._items.pop(0)
