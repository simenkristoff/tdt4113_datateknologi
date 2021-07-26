"""
The base Player class
"""

from project_2.action import Action

class Player():
    """
    The base Player class with no logic. Actions are based on user input.
    """
    def __init__(self, _id: int):
        """
        Initializes a generic Player

        :param _id:
        """
        self.name: str = ''
        self._id: int = _id
        self.points: float = 0.0
        self.actions: list = [
            'rock',
            'scissors',
            'paper'
        ]
        self.history: dict = {
            'points': [],
            'self': [],
            'opponent': [],
        }

    def enter_name(self):
        """
        Sets the name of the Player
        :return:
        """
        self.name = input(f'[Player {self._id}]: Please enter your name: ')

    def select_action(self):
        """
        Selects an action based on user input
        :return:
        """
        _x: int = 0
        # Loop if wrong input is entered
        # Valid: [1, 2, 3]
        print('Enter an action:\n1: Rock\n2: Scissors\n3: Paper ')
        while True:
            try:
                _x = int(input())
                if _x not in [1, 2, 3]:
                    raise ValueError()
            except ValueError:
                print('Invalid input, try again')
                continue
            else:
                break
        return Action(self.actions[_x-1])

    def recieve_result(self, points: float, own_action: str, opp_action: str):
        """
        Updates the players history based on the results of a game

        :param points: the points given to the Player for a given round
        :param own_action: the action the current player chose
        :param opp_action: the action the opponent chose
        :return:
        """
        self.history['points'].append(points)
        self.history['self'].append(own_action)
        self.history['opponent'].append(opp_action)

    def get_points(self):
        """
        Returns the Players points
        :return:
        """
        return self.history['points']

    def get_name(self):
        """
        Returns the players name
        :return:
        """
        return self.name
