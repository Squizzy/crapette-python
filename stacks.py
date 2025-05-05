from enum import Enum

class Stacks(Enum):
    """The various stacks in the game."""
    DECK:str = "Deck"
    CRAPETTE:str = "Crapette"
    REMAINDER:str = "Remainder"
    BIN:str = "Bin"
    TABLEAU_STACK:str = "Tableau Stack"
    FOUNDATION_STACK:str = "Foundation Stack"
    # The below do not contain cards, only stacks of cards
    TABLEAU:str = "Tableau"
    FOUNDATION:str = "Foundation"

class StacksInitSizes(Enum):
    """The number of cards in each stack at the start of the initialised game."""
    DECK:int = 52  # 52 cards in the deck
    CRAPETTE: int = 13  # 13 cards in the crapette stack
    REMAINDER: int = 35  # 35 cards in the remainder stack (52 - 13 - 4)
    BIN: int = 0  # 0 cards in the bin stack
    TABLEAU_STACK: int = 1  # 1 card per tableau stack
    FOUNDATION_STACK:int = 0  # 0 cards in the foundation stack
    # The below do not contain cards, only stacks of cards
    TABLEAU: int = 4  # 4 tableau stacks
    FOUNDATION: int = 4 # 4 foundation stacks