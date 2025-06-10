from deck import Deck
from stack_foundation import FoundationStack
from constants import Players
from stacks import Stacks, StacksInitSizes

# the class representing the player's Foundation area with its stacks

class FoundationStacks:
    _stack_name: Stacks
    _FoundationStacks: list[FoundationStack]
    _player_num: Players

    def __init__(self, deck:Deck, player_num: Players):
        if player_num not in [Players.PLAYER0, Players.PLAYER1]:
            raise ValueError(f"Error: Problem initiating Tableau stacks - player specified incorrect: {player_num}")
        self._stack_name = Stacks.FOUNDATION  # Name of the stack
        self._player_num =  player_num  # Player number of the stack owner
        self._FoundationStacks = []
        for _ in range(StacksInitSizes.FOUNDATION.value):
            foundation_stack = FoundationStack(deck, player_num)
            self._FoundationStacks.append(foundation_stack)