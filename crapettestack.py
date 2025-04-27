from cardstack import CardStack
from deck import Deck
from card import Card

class CrapetteStack(CardStack):
    _cards: list[Card]

    def __init__(self, deck: Deck):
        self._cards = []
        self._cards = deck.draw_n_cards(13)
        self._cards[len(self._cards) - 1].turn_face_up()

    # @property
    # def cards(self) -> list[Card]:
    #     """Return the list of cards in the Crapette Stack

    #     Returns:
    #         list[Card]: the list of cards
    #     """
    #     return self._cards

    # @property
    # def is_crapette_stack_empty(self) -> bool:
    #     """Confirms if there are still cards on the Crapette Stack or not

    #     Returns:
    #         bool: True if no card on the stack, False otherwise
    #     """
    #     return len(self._cards) == 0

    def can_be_added(self, card:Card) -> bool:
        """Check that a card can be added to the Crapette Stack

        Args:
            card (Card): the card to be checked

        Returns:
            bool: True if the card can be added, False if it cannot be added
        """
        if len(self._cards) == 0:
            return False
        
        if card.is_same_family(self._cards[len(self._cards) - 1]) and card.is_one_above_or_below(self._cards[len(self._cards) - 1]):
            return True
        
        return False
    
    def add_card(self, card:Card) -> bool:
        """ Add a card to the Crapette Stack after checking it can be added

        Args: 
            the card to be added

        Returns: 
            True if the card was added, False if card was not added
        """
        if self.can_be_added(card):
            card.turn_face_up()
            self._cards.append(card)
            return True
        return False
    
    # def force_add_card(self, card: Card) -> None:
    #     """Force add a card, for debug purpose

    #     Args:
    #         card (Card): The card to add
    #     """
    #     card.turn_face_up()
    #     self._cards.append(card)

    # def remove_top_card(self) -> bool:
    #     """Remove the top card from the Crapette Stack

    #     Returns:
    #         bool: True if the card was removed, False if no card was removed
    #     """
    #     if len(self._cards) == 0:
    #         return False
    #     else:
    #         try:
    #             self._cards.pop()
    #         except:
    #             print("Error removing a card from the Crapette Stack")
    #             return False
    #         if len(self._cards) > 0:
    #             self._cards[len(self._cards) - 1].turn_face_up()
    #         return True
         
    def draw_card(self) -> Card | None:
        """Draw the top card from the pack (but leaves it there)
        if the pile is empty or there is a problem drawing out a card, returns None.
        The drawn card is left on the crapette stack and will need to be removed with remove_card once it has been placed on another stack

        Returns:
            Card: the top card if the card could be drawn, otherwise none
        """
        if self.is_empty:
            print("No card on Crapette stack")
            return None
        
        try:
            drawn_card:Card = self._cards[len(self._cards) - 1]
        except:
            print("Could not draw card from Crapette stack")
            return None
        return drawn_card