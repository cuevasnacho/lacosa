from enum import Enum

class card_position(Enum):
    DECK = 1
    DISCARD = 2
    PLAYER = 3

class player_roles(Enum):
    THE_THING = 1
    HUMAN = 2
    INFECTED = 3

class match_status(Enum):
    NOT_INITIALIZED = 1
    INITIALIZED= 2
    FINISHED = 3

class cards_subtypes(Enum):
    INFECTION = 1
    ACTION = 2
    DEFENSE = 3
    OBSTACLE = 4


class results(Enum):
    SUCSSESFUL = 1
    ERROR = 0
#ejemplo de como acceder al valor : card:position.DECK.value