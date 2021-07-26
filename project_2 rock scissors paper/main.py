"""
The main wrapper for the application
"""
import re
import traceback

from single_game import SingleGame
from tournament import Tournament
from players import Player, Random, Sequential, MostCommon, Historian


def read_flags(cmd: str):
    """
    Reads the flags from the command line
    :param cmd:
    :return:
    """
    _m = re.findall(r'^(\w+){1}|(\-\w*\=\d*)|(\-\w+)', cmd)
    flags: list = []
    for i in range(len(_m)):
        for j in range(3):
            val = _m[i][j]
            if len(val) > 0:
                flags.append(val.replace('-', ''))
    flags.reverse()
    return flags


def initialize_players(player_flags: list):
    """
    Initializes the players based on the flags from the command line
    :param player_flags:
    :return:
    """
    players = [None, None]
    for i in range(2):
        val = ''.join(filter(str.isalpha, player_flags[i]))
        if val == 'rand':
            players[i] = Random(i)
        elif val == 'mocom':
            players[i] = MostCommon(i)
        elif val == 'hist':
            remember = player_flags[i].split('=')[1]
            if not remember.isdigit():
                remember = 1
            players[i] = Historian(i, int(remember))
        elif val == 'seq':
            players[i] = Sequential(i)
        else:
            players[i] = Player(i)
    return players


def filter_player_flags(flags_list):
    """
    Filter the flags referencing players from the list of flags
    :param flags_list:
    :return:
    """
    ref = ['rand', 'mocom', 'hist', 'seq', 'player']
    player_flags: list = []
    non_player_flags: list = []
    for i in range(len(flags_list)):
        # Remove everything except letters
        val = ''.join(filter(str.isalpha, flags_list[i]))
        if val in ref:
            player_flags.append(flags_list[i])
        else:
            non_player_flags.append(flags_list[i])

    return player_flags, non_player_flags


def handle_help():
    """
    Prints the helpers interface for the command line
    :return:
    """
    print('[HELP]')
    print('[INITIATORS]\n game - Creates a game new game between two players.'
          ' See arguments under [PLAYERS]\n'
          'tournament - Creates a tournament between two players where \'num=??\''
          ' defines number of rounds to play\n'
          'default is 100. See arguments under [PLAYERS]\n')
    print('[PLAYERS]\n player - defines a real life player\n'
          ' rand - defines a player of type Random\n'
          'mocom - defines a player of type Most Common\n'
          ' seq - defines a player of type Sequential\n'
          'hist=?? - defines a player of type Historian.'
          ' Takes in parameter for the length of sequence to remember, '
          'default is 1')
    print('[EXAMPLE]: tournament -rand -hist=30 -num=10')


def handle_game(flags: list):
    """
    Launches a game based on input from the command line
    :param flags:
    :return:
    """
    player_flags, flags = filter_player_flags(flags)
    player1, player2 = initialize_players(player_flags)

    player1.enter_name()
    player2.enter_name()

    try:
        game = SingleGame(player1, player2)
        game.perform_game()
    except TypeError:
        print('[ERROR] failed to start Game')
        traceback.print_exc()


def handle_tournament(flags: list):
    """
    Launches a tournament based on input from the command line
    :param flags:
    :return:
    """
    player_flags, flags = filter_player_flags(flags)
    player1, player2 = initialize_players(player_flags)
    number_of_games = 100

    if ''.join(filter(str.isalpha, flags[0])) == 'num':
        val = flags[0].split('=')[1]
        if val.isdigit():
            number_of_games = val

    try:
        tournament = Tournament(player1, player2, int(number_of_games))
        tournament.arrange_tournament()
    except TypeError:
        print('[ERROR] failed to start Tournament')
        traceback.print_exc()

def main():
    """
    Starts the main loop and command line interface.
    Example input: tournament -rand -hist=3 -num=100
    :return:
    """
    while True:
        print('Type \'help\' for more information')
        cmd = input("[CMD]: ").lower()
        flags: list = read_flags(cmd)
        initiator = flags.pop()

        if initiator == 'help':
            handle_help()
        elif initiator == 'game':
            handle_game(flags)
        elif initiator == 'tournament':
            handle_tournament(flags)
        else:
            print('Invalid command. Please enter \'help\' for more information.')


if __name__ == "__main__":
    main()
