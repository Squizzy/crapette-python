from cardstack import CardStack, Transferred_Card, Stacks
from deck import Deck
from card import Card

class CrapetteStack(CardStack):
    _stack_name: Stacks = Stacks.CRAPETTE
    _cards: list[Card] # probably redundant as defined in cardstack
    _player_num: int  # probably redundant as defined in cardstack
    _drawn_card: Transferred_Card


    def __init__(self, deck: Deck, player_num: int):
        self._player_num = player_num
        self._cards = []
        self._cards = deck.draw_n_cards(13)
        if len(self._cards) != 13:
            raise ValueError(f"Error: The {self._stack_name} deck should have 13 cards, but it has {len(self._cards)} cards")
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

    def can_be_added(self, proposed_card:Transferred_Card) -> bool:
        """Check that a card can be added to the Crapette Stack

        Args:
            card (Card): the card to be checked
            player_num: The ID of the player wanting to place the card

        Returns:
            bool: True if the card can be added, False if it cannot be added
        """
        
        # If there is no card, no more card can be added
        if len(self._cards) == 0:
            return False
        
        # If the card is being plauyed by the player
        #   if the card comes from this stack
        #     that's fine
        if proposed_card._from_player is self.is_player:
            if proposed_card._from_stack_name in [Stacks.CRAPETTE]:
                return True
        
        # If the card is being played picked by the opponent
        else:
            #   if it does not adhere to the stacking rule (same family and  1+ or 1-)
            #       then the card can't be added
            if not proposed_card._card.is_one_above_or_below(self.top_card) or not proposed_card._card.is_same_family(self.top_card):
                return False
            
            #   If the stack was from the opponent's crapette or remainder stack
            #       That's fine
            if proposed_card._from_stack_name in [Stacks.CRAPETTE, Stacks.REMAINDER] \
                and proposed_card._from_stack_owner is not self.is_player:
                    return True
            
            #   or if the card was from the tableau (not caring for who's)
            #       That's fine
            elif proposed_card._from_stack_name in [Stacks.TABLEAU]:
                    return True                
        
        # In any other case, card can't be added
        return False


        # # Then it can only be placed if it comes from the same stack.
        # # This is the case is the top_card is not returned 
        # # TODO: check top_card is not the same card
        # if source_player_num == self._player_num:

        #     if not self.top_card.face_up:
        #         return True
            
        # if card.is_same_family(self._cards[len(self._cards) - 1]) and card.is_one_above_or_below(self._cards[len(self._cards) - 1]):
        #     return True
        
        # return False
    
    def add_card(self, proposed_card:Transferred_Card) -> bool: 
        """ Add a card to the Crapette Stack after checking it can be added

        Args: 
            the card to be added

        Returns: 
            True if the card was added, False if card was not added
        """
        if self.can_be_added(proposed_card):
            proposed_card._card.turn_face_up()
            self._cards.append(proposed_card._card)
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
         
    # def draw_card(self) -> Card | None:
    #     """Draw the top card from the pack (but leaves it there)
    #     if the pile is empty or there is a problem drawing out a card, returns None.
    #     The drawn card is left on the crapette stack and will need to be removed with remove_card once it has been placed on another stack

    #     Returns:
    #         Card: the top card if the card could be drawn, otherwise none
    #     """
    #     if self.is_empty:
    #         print("No card on Crapette stack")
    #         return None
        
    #     try:
    #         drawn_card:Card = self._cards[len(self._cards) - 1]
    #     except:
    #         print("Could not draw card from Crapette stack")
    #         return None
    #     return drawn_card