from cardstack import CardStack, Stacks, TransferredCard, StacksInitSizes
from deck import Deck
from card import Card, TransferredNCards
from player import Players

class TableauStack(CardStack):
    _stack_name: Stacks
    _cards: list[Card]
    _selected_cards: list[Card]
    _player_num: Players

    def __init__(self, deck: Deck, player_num:Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Tableau stack - player specified incorrect: {player_num}")
        self._stack_name = Stacks.TABLEAU_STACK  # Name of the stack
        self._player_num = player_num  # Player number of the stack owner
        self._cards = []  # create the empty stack of cards
        first_card: Card = deck.draw_n_cards(StacksInitSizes.TABLEAU_STACK.value)[0]  # draw the first card from the deck
        if self.size != StacksInitSizes.TABLEAU_STACK.value:
            raise ValueError(f"Error: The {self.what_stack_am_i} deck should have {StacksInitSizes.TABLEAU_STACK.value} cards, but it has {len(self._cards)} cards")
        first_card.turn_face_up() # turn the first card face up
        self._cards.append(first_card)  # add the first card to the stack
        self._selected_cards = []  # create the empty list of selected cards

    @property
    def cards(self) -> list[Card]:
        return self._cards

    def position_in_stack(self, card) -> int | None:
        if card in self._cards:
            position: int = self._cards.index(card)
            return position
        else:
            return None

    # Check rule for adding a card to the Tableau stack
    def can_be_added(self, proposed_card:TransferredCard) -> bool:
        """Check that a card can be added to the Tableau stack

        Args:
            proposed_card (Card): the card to be checked

        Returns:
            bool: True if the card can be added, False if it cannot be added
        """

        # If no card in this stack, regardless of who is placing the card, no issue
        if self.is_empty:
            return True

        # Otherwise (card already present),
        #   If the card is one below in value from the card already there, and it is not the same colour
        #       That's fine
        if self.top_card.is_one_above(proposed_card.card) and not self.top_card.is_same_colour(proposed_card.card):
            return True
        
        # Otherwise, can't add card
        return False

    def add_n_cards(self, proposed_cards: TransferredNCards) -> bool:
        """Adds the proposed cards to the stack if they can be added
        Args:
            proposed_cards (TransferredNCards): The list of transferred cards to be added

        Returns:
            bool: True if the cards were added, False if the cards were not added
        """
        #If the bottom card of the proposed cards can be added (bottom_card is of format transferred_card)
        #   then add all the cards to the stack
        if self.can_be_added(proposed_cards.bottom_card):
            for transferred_card in proposed_cards.cards:
                self.add_card(transferred_card)
            return True
        return False

    def select_cards(self, card: Card) -> list[Card]|None:
        """Selects all the cards from the card provided to the top of the stack
        It does not remove the cards from the stack

        Args:
            card (Card): The card from which to select

        Returns:
            list[Card]: the card from which to select until the top of the pile, None if the card is not in the stack
        """
        position = self.position_in_stack(card)

        if not position:
            return None
        
        # TODO: It might be useful to use a parent/child linking instead but this'll do for now
        self._selected_cards = []
        self._selected_cards = self._cards[position:]
        return self._selected_cards
    
    @property
    def selected_cards(self) -> list[Card]:
        """Returns the list of selected cards
        
        Returns:
            list[Card]: the selected cards if cards are selected.
        """
        return self._selected_cards

    @property
    def selected_cards_quantity(self) -> int:
        """Returns the number of selected cards"""
        return len(self._selected_cards)
    
    def deselect_cards(self) -> None:
        """Deselects the selected cards"""
        self._selected_cards = []

    def remove_selected_cards_from_stack(self) -> bool:
        """Remove the selected cards from the stack but not not empty the selected_cards list
        
        Returns:
            bool: True if the cards were removed, False if not
        """
        # If no card was selected, no issue
        if self.selected_cards_quantity == 0:
            return True
        
        # If not all the selected cards are in the stack
        if not set(self.selected_cards).issubset(self.cards):
            # Then there is a problem, raise it
            raise ValueError(f"Error removing the selected card(s) from the Tableau stack: {self.selected_cards} not in {self.cards}")
            # Remove the selected cards from the stack
            
        # Then if all 
        for card in self.selected_cards: 
            self._cards.remove(card)
        return True
    
        
        # # going the long way just in case there is a problem
        # inverted_selected_cards: list[Card] = self._selected_cards[::-1]
        # for card in inverted_selected_cards:
        #     if card == self.top_card:
        #         self.remove_top_card()
        #     else:
        #         print("Error removing the selected card(s) from the Tableau stack")
        #         return False
        # return True