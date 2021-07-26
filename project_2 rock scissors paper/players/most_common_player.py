"""
The MostCommon Player class
"""
import random
import itertools
import operator

from project_2.action import Action
from project_2.players import Player


class MostCommon(Player):
    """
    The player MostCommon chooses an action based on the opponents most common choices.
    """
    # Defines which action to choose based on the key
    table: dict = {
        "scissors": "rock",
        "rock": "paper",
        "paper": "scissors"
    }

    def enter_name(self):
        """
        Generates a name for the player
        :return:
        """
        self.name = f'MostCommon {self._id}'

    def get_most_common(self):
        """
        Sorts the most common action the opponent has chosen
        :return:
        """
        sorted_list = sorted((x, i) for i, x in enumerate(self.history['opponent']))
        groups = itertools.groupby(sorted_list, key=operator.itemgetter(0))
        def _auxfun(_g):
            _item, iterable = _g
            count = 0
            min_index = len(self.history['opponent'])
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            return count, -min_index
            # pick the highest-count/earliest item
        return max(groups, key=_auxfun)[0]

    def select_action(self):
        """
        Selects an action based on the opponents history of choices.
        If it's the first round, the player will pick a random action.
        :return:
        """
        if len(self.history['opponent']) > 0:
            return Action(self.table[self.get_most_common()])
        return Action(self.actions[random.randint(0, 2)])
