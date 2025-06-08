from enum import Enum

# The enum representing the players
class Players(Enum):
    PLAYER1 = 0
    PLAYER2 = 1
    CARDSTACK = 2 # mostly for debugging purposes for the moment
    ERROR = -1