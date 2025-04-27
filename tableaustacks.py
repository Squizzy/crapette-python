from deck import Deck
from tableaustack import TableauStack

class TableauStacks:
    _TableauStacks: list[TableauStack]

    def __init__(self, deck:Deck):
        self._TableauStacks = []
        for _ in range(4):
            TS = TableauStack(deck)
            self._TableauStacks.append(TS)