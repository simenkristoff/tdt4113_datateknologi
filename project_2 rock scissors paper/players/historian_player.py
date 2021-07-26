"""
The Historian Player class
"""
import random
import itertools
import operator

from project_2.action import Action
from project_2.players.player import Player

class Historian(Player):
    """
    The player Historian chooses an action based on the opponents sequence of choices.
    """
    # Defines which action to choose based on the key
    table: dict = {
        "scissors": "rock",
        "rock": "paper",
        "paper": "scissors"
    }

    def __init__(self, _id: int, remember: int):
        """
        Initializes a Historian Player

        :param _id:
        """
        self.remember = remember
        self.name = ''
        super().__init__(_id)

    def enter_name(self):
        """
        Generates a name for the player
        :return:
        """
        self.name = f'Historian {self._id}'

    def select_by_history(self):
        """
        Finds sequences and pick an action to counter the opponents most probable next move
        :return:
        """
        # Obtain the recent choices made by opponent
        next_choice: list = []
        _h = self.history['opponent']
        sequence = _h[-self.remember:]
        # Find the all following moves based on the sequence
        for i in range(len(_h) - (self.remember + 1), 0, -1):
            if _h[i:i + self.remember] == sequence:
                next_index = i + self.remember
                if self.remember == 1:
                    return self.table[_h[next_index]]

                next_choice.append(_h[next_index])
        # If there are any moves to choose from, pick the one with most occurences
        if len(next_choice) > 0:
            sorted_list = sorted((x, i) for i, x in enumerate(next_choice))
            groups = itertools.groupby(sorted_list, key=operator.itemgetter(0))

            def _auxfun(_g):
                _item, iterable = _g
                count = 0
                min_index = len(next_choice)
                for _, where in iterable:
                    count += 1
                    min_index = min(min_index, where)
                return count, -min_index
                # pick the highest-count/earliest item

            return self.table[max(groups, key=_auxfun)[0]]
        else:
            return self.actions[random.randint(0, 2)]

    def select_action(self):
        """
        Selects an action
        :return:
        """
        if len(self.history['opponent']) > self.remember + 1:
            return Action(self.select_by_history())
        return Action(self.actions[random.randint(0, 2)])
