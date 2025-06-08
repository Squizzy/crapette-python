# from enum import Enum
from deck import Deck
from stack_crapette import CrapetteStack
from stack_remainder import RemainderStack
from stack_bin import BinStack
# from stacks_tableau import TableauStacks
from stacks_tableau import TableauStack
# from stacks_foundation import FoundationStacks
from stack_foundation import FoundationStack
from constants import Players

from icecream import ic # type: ignore


DEBUG: bool = False
def log_message(message: str):
    if DEBUG:
        ic(f"player: {message}")
        
class Player:
    _player_num: Players
    _crapette: CrapetteStack
    _remainder: RemainderStack
    _bin: BinStack
    _tableau0: TableauStack
    _tableau1: TableauStack
    _tableau2: TableauStack
    _tableau3: TableauStack
    _foundation0: FoundationStack
    _foundation1: FoundationStack
    _foundation2: FoundationStack
    _foundation3: FoundationStack
    
    
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

        self._tableau0 = TableauStack(deck, player_num)        
        self._tableau1 = TableauStack(deck, player_num)        
        self._tableau2 = TableauStack(deck, player_num)        
        self._tableau3 = TableauStack(deck, player_num)        
        log_message(f"{self._tableau0.size=}")
        log_message(f"{self._tableau1.size=}")
        log_message(f"{self._tableau2.size=}")
        log_message(f"{self._tableau3.size=}")
        log_message(f"{deck.size=}")

        self._remainder = RemainderStack(deck, player_num)
        log_message(f"{self._remainder.size=}")
        log_message(f"{deck.size=}")

        self._bin = BinStack(player_num)
        log_message(f"{self._bin.size=}")
        log_message(f"{deck.size=}")

        self._foundation0 = FoundationStack(deck, player_num)
        self._foundation1 = FoundationStack(deck, player_num)
        self._foundation2 = FoundationStack(deck, player_num)
        self._foundation3 = FoundationStack(deck, player_num)
        log_message(f"{self._foundation0.size=}")
        log_message(f"{self._foundation1.size=}")
        log_message(f"{self._foundation2.size=}")
        log_message(f"{self._foundation3.size=}")
        log_message(f"{deck.size=}")
        