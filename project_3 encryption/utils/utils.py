""" Util module """
from random import randint


def create_alphabet():
    """
    Creates a bi-directional alphabet where each key-value pair is reflexive.

    :return: bi-directional alphabet
    """
    table = {chr(i): i - 32 for i in range(32, 127)}
    table.update({i - 32: chr(i) for i in range(32, 127)})
    return table


def random_word():
    """
    Returns a single random word.

    :return: random word
    """
    with open('res/english_words.txt', 'r+') as _f:
        words = _f.read().splitlines()
    return words[randint(0, len(words) - 1)]


def random_message(message_len: int):
    """
    Returns a random message.

    :param message_len: the word length
    :return: random message
    """
    message = []
    for _ in range(message_len):
        message.append(random_word())
    return ' '.join(message)


def load_dictionary():
    """
    Creates a dictionary of the words in english_words.txt

    :return: dictionary
    """
    with open('res/english_words.txt', 'r+') as _f:
        words = _f.read().splitlines()
    return {word: True for word in words}
