"""State enum module"""
from enum import Enum


class State(Enum):
    """FSM state enum"""
    INIT = 0
    READ = 1
    VERIFY = 2
    ACTIVE = 3
    READ2 = 4
    READ3 = 5
    LED = 6
    TIME = 7
    EXIT = 8
