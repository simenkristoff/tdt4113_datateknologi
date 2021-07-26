"""
Module for a single Game instance
"""

from action import Action
from players import Player


class SingleGame:
    """
    The class SingleGame handles logic for simulating a game instance
    """
    winner: Player = None
    p1_action: Action = None
    p2_action: Action = None

    def __init__(self, player1: Player, player2: Player):
        """
        Initializes a Game instance
        :param player1:
        :param player2:
        """
        self.p1_points = 0.0
        self.p2_points = 0.0
        self.player1 = player1
        self.player2 = player2

    def perform_game(self):
        """
        Gets an action from each player and checks the result
        :return:
        """
        self.p1_action = self.player1.select_action()
        self.p2_action = self.player2.select_action()
        self.winner = self.decide_game()
        self.show_result()
        self.send_feedback()

    def decide_game(self):
        """
        Decides which player has won the game
        :return:
        """
        _a1 = self.p1_action
        _a2 = self.p2_action
        if _a1 == _a2:
            self.p1_points, self.p2_points = 0.5, 0.5
            return None
        elif _a1 > _a2:
            self.p1_points = 1.0
            return self.player1
        else:
            self.p2_points = 1.0
            return self.player2

    def send_feedback(self):
        """
        Sends feedback from the current round to the participating players
        :return:
        """
        self.player1.recieve_result(self.p1_points, self.p1_action.get_value(),
                                    self.p2_action.get_value())
        self.player2.recieve_result(self.p2_points, self.p2_action.get_value(),
                                    self.p1_action.get_value())

    def show_result(self):
        """
        Prints information of the Game in the console
        :return:
        """
        print(f'[{self.player1.get_name()}] has chosen {self.p1_action.get_value()}')
        print(f'[{self.player2.get_name()}] has chosen {self.p2_action.get_value()}')
        if self.winner is None:
            print('There\'s a tie')
        else:
            print(f'The winner is {self.winner.get_name()}')
