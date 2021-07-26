"""Container module"""


class Container:
    """Class Container"""

    def __init__(self):
        self._items = []

    def size(self):
        """
        Return number of elements in self._items
        :return: the size of the container
        """
        return len(self._items)

    def is_empty(self):
        """
        Check if self._items is empty
        :return: True if self._items is empty, else False
        """
        return not self._items

    def push(self, item):
        """
        Add an item to the end of self._items
        :param item: the item to add
        """
        self._items.append(item)

    def pop(self):
        """
        Pop off the correct element of self._items, and return it.
        This method differs between subclasses, hence is not implemented in
        the superclass
        :return: the first element in the data structure
        """
        raise NotImplementedError("Pop not implemented yet!")

    def peek(self):
        """
        Return the top element without removing it.
        This method differs between subclasses, hence is not implemented in
        the superclass
        :return: the top element
        """
        raise NotImplementedError("Peek not implemented yet!")

    def clear(self):
        """
        Clears the items
        :return: None
        """
        self._items = []

    def __str__(self):
        """
        Print the elements
        :return: string of items
        """
        return str(self._items)
