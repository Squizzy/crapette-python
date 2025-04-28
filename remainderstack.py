from cardstack import CardStack
from card import Card
from deck import Deck

class RemainderStack(CardStack):
    _cards: list[Card]

    def __init__(self, deck: Deck):
        self._cards = []
        self._cards = deck.draw_remaining_cards()

    # @property
    # def size(self) -> int:
    #     return len(self._cards)
    
    # @property
    # def top_card(self):
    #     return self._cards[len(self._cards) - 1]