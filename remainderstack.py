from cardstack import CardStack
from stacks import Stacks, StacksInitSizes
from player import Players
from card import Card
from deck import Deck

class RemainderStack(CardStack):
    _stack_name: Stacks
    _cards: list[Card]
    _player_num: Players

    def __init__(self, deck: Deck, player_num: Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Remainder stack - player specified incorrect: {player_num}")
        self._stack_name = Stacks.REMAINDER  # Name of the stack
        self._player_num = player_num  # Player number of the stack owner
        self._cards = []  # create the empty stack of cards
        self._cards = deck.draw_remaining_cards()  # draw the remaining cards from the deck
        if len(self._cards) != StacksInitSizes.REMAINDER.value:  # check the number of cards in the stack
            raise ValueError(f"Error: The {self.what_stack_am_i} deck should have {StacksInitSizes.REMAINDER.value} cards, but it has {self.size} cards")
    
    def reload_from_binstack(self, binstack_cards: list[Card]) -> bool:
        """Reloads the Remainder stack from the Bin stack.
        This method should only be called when the Bin stack is empty.
        The cards are added to the Remainder stack in reverse order, and they are turned face down.
        This method does not empty the Bin stack
        
        Args:
            binstack_cards (list[Card]): The list of cards to be added to the Remainder stack
            
        Returns:
            bool: True if the cards were added, False if the stack was not empty
        """
        if self.size != 0:
            return False
        
        new_stack: list[Card] = binstack_cards
        new_stack.reverse()
        for card in new_stack:
            card.turn_face_down()
            self._cards.append(card)
        return True