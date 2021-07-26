"""
The Random Player class
"""
import random

from project_2.action import Action
from project_2.players.player import Player


class Random(Player):
    """
    The player Random chooses random actions.
    """
    def enter_name(self):
        """
        Generates a name for the player
        :return:
        """
        self.name = f'Random {self._id}'

    def select_action(self):
        """
        Returns a random action
        :return:
        """
        return Action(self.actions[random.randint(0, 2)])
