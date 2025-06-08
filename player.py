# from enum import Enum
from deck import Deck
from stack_crapette import CrapetteStack
from stack_remainder import RemainderStack
from stack_bin import BinStack
from stacks_tableau import TableauStacks
from stacks_foundation import FoundationStacks
from constants import Players

from icecream import ic # type: ignore

# # The enum representing the players
# class Players(Enum):
#     PLAYER1 = 0,
#     PLAYER2 = 1,
#     CARDSTACK = 2 # mostly for debugging purposes for the moment


DEBUG: bool = False
def log_message(message: str):
    if DEBUG:
        ic(f"player: {message}")
        
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
        log_message(f"{deck.size=}")
        #deck.shuffle()
        
        self._crapette = CrapetteStack(deck, player_num)
        log_message(f"{self._crapette.size=}")
        log_message(f"{deck.size=}")

        self._tableau = TableauStacks(deck, player_num)        
        log_message(f"{self._tableau._TableauStacks[0].size=}")
        log_message(f"{deck.size=}")

        self._remainder = RemainderStack(deck, player_num)
        log_message(f"{self._remainder.size=}")
        log_message(f"{deck.size=}")

        self._bin = BinStack(player_num)
        log_message(f"{self._bin.size=}")
        log_message(f"{deck.size=}")

        self._foundation = FoundationStacks(deck, player_num)
        log_message(f"{self._foundation._FoundationStacks[0].size=}")
        log_message(f"{deck.size=}")
        