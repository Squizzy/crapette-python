from deck import Deck
from tableaustack import TableauStack
from player import Players
from stacks import Stacks, StacksInitSizes

class TableauStacks:
    _stack_name: Stacks
    _TableauStacks: list[TableauStack]
    _player_num: Players

    def __init__(self, deck:Deck, player_num: Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Tableau stacks - player specified incorrect: {player_num}")
        self._stack_name = Stacks.TABLEAU_STACK  # Name of the stack
        self._player_num =  player_num  # Player number of the stack owner
        self._TableauStacks = []
        for _ in range(StacksInitSizes.TABLEAU.value):
            tableau_stack = TableauStack(deck, player_num)
            self._TableauStacks.append(tableau_stack)