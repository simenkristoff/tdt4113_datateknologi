"""
Module for Actions
"""
class Action:
    """
    Handles the available actions in Rock, Scissors, Paper
    """
    table = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    def __init__(self, choice):
        """
        Initializes an action, and validates if the action is correct.
        :param choice:
        """
        if not self.table.get(choice):
            raise TypeError('Invalid action')
        self.choice = choice
        self.beats = self.table[choice]

    def get_value(self):
        """
        Returns the string value of the action
        :return:
        """
        return self.choice

    def __eq__(self, opponent):
        """
        Returns true if the action is equivalent to another action
        :param opponent:
        :return:
        """
        return self.choice == opponent.choice

    def __gt__(self, opponent):
        """
        Returns true if the action is greater than another action
        :param opponent:
        :return:
        """
        return self.beats == opponent.choice
