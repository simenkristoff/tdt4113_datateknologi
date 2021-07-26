"""
Module for a Tournament
"""

import matplotlib.pyplot as plt
from single_game import SingleGame
from players import Player


class Tournament:
    """
    The class Tournament handles logic for simulating many game instances
    """
    def __init__(self, player1: Player, player2: Player, number_of_games: int):
        """
        Initializes a tournament between two players
        :param player1: Player 1
        :param player2: Player 2
        :param number_of_games: Amount of games to simulate
        """
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games

    def arrange_singlegame(self):
        """
        Runs a single game
        :return:
        """
        game = SingleGame(self.player1, self.player2)
        game.perform_game()

    def arrange_tournament(self):
        """
        Launches the tournamens
        :return:
        """
        self.player1.enter_name()
        self.player2.enter_name()
        for _i in range(self.number_of_games):
            self.arrange_singlegame()

        self.plot_points()

    def plot_points(self):
        """
        Plot the results to a graph
        :return:
        """
        point_history = self.player1.get_points()
        ppg = [] # points per game
        points = 0

        for i in range(self.number_of_games):
            points += point_history[i]
            ppg.append(points / (i + 1))

        plt.plot(ppg)
        plt.plot([0.5] * self.number_of_games, '--')
        plt.ylim(0, 1)

        plt.title(f'[{self.player1.get_name()}] Average points per game')

        plt.xlabel('Iteration')
        plt.ylabel("Average points per game")
        plt.show()
