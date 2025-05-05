from enum import Enum
from deck import Deck
from crapettestack import CrapetteStack
from remainderstack import RemainderStack
from binstack import BinStack
from tableaustacks import TableauStacks
from foundationstacks import FoundationStacks

# The enum representing the players
class Players(Enum):
    PLAYER1 = 0,
    PLAYER2 = 1,
    CARDSTACK = 2 # mostly for debugging purposes for the moment


class Player:
    _player_num: Players
    _crapette: CrapetteStack
    _remainder: RemainderStack
    _bin: BinStack
    _tableau: TableauStacks
    _foundation: FoundationStacks
    
    
    def __init__(self, player_num: Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Tableau stacks - player specified incorrect: {player_num}")
        self._player_num =  player_num  # Player number of the stack owner
        deck = Deck(player_num)
        self._crapette = CrapetteStack(deck, player_num)
        self._remainder = RemainderStack(deck, player_num)
        self._bin = BinStack(deck, player_num)
        self._tableau = TableauStacks(deck, player_num)
        self._foundation = FoundationStacks(deck, player_num)
        