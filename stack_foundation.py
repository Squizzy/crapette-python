from cardstack import CardStack
from stacks import Stacks, StacksInitSizes
from deck import Deck
from card import Card, TransferredCard, Rank, Suit
from constants import Players

# the class representing one foundation stack object in the game

class FoundationStack(CardStack):
    _stack_name: Stacks
    _cards: list[Card]
    _selected_cards: list[Card]
    _player_num: Players

    def __init__(self, deck: Deck, player_num:Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Tableau stack - player specified incorrect: {player_num}")
        self._stack_name = Stacks.FOUNDATION_STACK  # Name of the stack
        self._player_num = player_num  # Player number of the stack owner
        self._cards = []  # create the empty stack of cards
        # first_card: Card = deck.draw_n_cards(StacksInitSizes.FOUNDATION_STACK.value)[0]  # draw the first card from the deck
        # first_card.turn_face_up() # turn the first card face up
        # self._cards.append(first_card)  # add the first card to the stack
        # if self.size != StacksInitSizes.FOUNDATION_STACK.value:
        #     raise ValueError(f"Error: The {self.what_stack_am_i} deck should have {StacksInitSizes.TABLEAU_STACK.value} cards, but it has {len(self._cards)} cards")
        self._selected_cards = []  # create the empty list of selected cards


    # Check rule for adding a card to the Foundation stack
    def can_be_added(self, proposed_card:TransferredCard) -> bool:
        """Check that a card can be added to the Foundation stack:
        If the stack is empty, any Ace can be added.
        If the card is not empty, the card to add must be same suit and +1 from the top card
        any player can add to any foundation stack

        Args:
            proposed_card (Card): the card to be checked

        Returns:
            bool: True if the card can be added, False if it cannot be added
        """

        # If no card in this stack, regardless of who is placing the card, no issue
        if self.is_empty:
            if proposed_card.card.rank == Rank.ACE:
                return True
            else:
                return False

        # Otherwise (card already present),
        #   If the card is one above in value from the top card, 
        #   and it is not the same suit
        #       That's fine
        if self.top_card.is_one_below(proposed_card.card) and self.top_card.suit == proposed_card.card.suit:
            return True
        
        # Otherwise, can't add card
        return False
