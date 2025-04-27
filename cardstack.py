from card import Card

class CardStack:
    
    @property
    def size(self) -> int:
        return len(self._cards)
    
    @property
    def top_card(self) -> Card:
        return self._cards[len(self._cards) - 1]
    
    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0
    

    @property
    def cards(self) -> list[Card]:
        """Return the list of cards in the Crapette Stack

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
            except:
                print("Error removing a card from the Stack")
                return False
            if len(self._cards) > 0:
                self._cards[len(self._cards) - 1].turn_face_up()
            return True