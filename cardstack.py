from card import Card

class CardStack:
    _cards: list[Card]
    _stackname:str = "Parent Stack Class"
    # _stackname:str
    
    @property
    def size(self) -> int:
        return len(self._cards)
    
    @property
    def what_stack_am_i(self):
        return self._stackname
    
    @property
    def top_card(self) -> Card:
        return self._cards[len(self._cards) - 1]
    
    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0
    
    # This method contains the specific stack's rules for adding a card
    # So needs to be overridden
    def can_be_added(self, card: Card) -> bool:
        print("The method 'can_be_added' has not yet been overridden, but it must be")
        print(card)
        return False

    @property
    def cards(self) -> list[Card]:
        """Return the list of cards in the Stack

        Returns:
            list[Card]: the list of cards
        """
        return self._cards

    def add_card(self, card: Card) -> bool:
        if self.can_be_added(card):
            self._cards.append(card)
            return True
        return False
    
    def force_add_card(self, card: Card) -> None:
        """Force add a card, for debug purpose

        Args:
            card (Card): The card to add
        """
        card.turn_face_up()
        self._cards.append(card)

    def remove_top_card(self) -> bool:
        """Remove the top card from the Stack

        Returns:
            bool: True if the card was removed, False if no card was removed
        """
        if len(self._cards) == 0:
            return False
        else:
            try:
                self._cards.pop()
            except Exception as e:
                print(f"Error {e} removing a card from the {self._stackname} stack")
                return False
            if len(self._cards) > 0:
                self._cards[len(self._cards) - 1].turn_face_up()
            return True
        
    def draw_top_card(self) -> Card | None:
        """Draw the top card from the pack (but leaves it there)
        if the pile is empty or there is a problem drawing out a card, returns None.
        The drawn card is left on the crapette stack and will need to be removed with remove_card once it has been placed on another stack

        Returns:
            Card: the top card if the card could be drawn, otherwise none
        """
        if self.is_empty:
            print(f"No card on {self._stackname} stack")
            return None
        
        try:
            drawn_card:Card = self._cards[len(self._cards) - 1]
        except Exception as e:
            print(f"error {e}: Could not draw card from {self._stackname} stack")
            return None
        return drawn_card