from deck import Deck
from tableaustack import TableauStack

class TableauStacks:
    _TableauStacks: list[TableauStack]
    _player_num: int

    def __init__(self, deck:Deck, player_num: int):
        self._player_num =  player_num
        self._TableauStacks = []
        for _ in range(4):
            TS = TableauStack(deck, player_num)
            self._TableauStacks.append(TS)