from enum import Enum

# The enum representing the various stacks in the game
class Stacks(Enum):
    """The various stacks in the game."""
    DECK = "Deck"
    CRAPETTE = "Crapette"
    REMAINDER = "Remainder"
    BIN = "Bin"
    TABLEAU_STACK = "Tableau Stack"
    FOUNDATION_STACK = "Foundation Stack"
    # The below do not contain cards, only stacks of cards
    TABLEAU = "Tableau"
    FOUNDATION = "Foundation"

# The enum represeting the number of cards (or stacks) per stack at initialisatio 
class StacksInitSizes(Enum):
    """The number of cards in each stack at the start of the initialised game."""
    DECK = 52  # 52 cards in the deck
    CRAPETTE = 13  # 13 cards in the crapette stack
    REMAINDER = 35  # 35 cards in the remainder stack (52 - 13 - 4)
    BIN = 0  # 0 cards in the bin stack
    TABLEAU_STACK = 1  # 1 card per tableau stack
    FOUNDATION_STACK = 0  # 0 cards in the foundation stack
    # The below do not contain cards, only stacks of cards
    TABLEAU = 4  # 4 tableau stacks
    FOUNDATION = 4 # 4 foundation stacks