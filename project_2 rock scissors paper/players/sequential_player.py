"""
The Sequential Player class
"""

from project_2.action import Action
from project_2.players.player import Player


class Sequential(Player):
    """
    The player Sequential chooses an action in sequence of "rock", "scissors", "paper"
    """
    # Initializes first index: 'rock'
    last_index: int = 0
    def enter_name(self):
        """
        Generates a name for the player
        :return:
        """
        self.name = f'Sequential {self._id}'

    def select_action(self):
        """
        Selects an action based on sequence of "rock", "scissors", "paper".
        :return:
        """
        # Checks if index is within range
        if self.last_index > 2:
            self.last_index = 0
        action = Action(self.actions[self.last_index])
        # Increments index by 1
        self.last_index += 1
        return action
