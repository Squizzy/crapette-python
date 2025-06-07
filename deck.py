from random import shuffle
from card import Card, Suit, Rank
from constants import Players


# The class presenting the full deck of card object

class Deck:
    _cards: list[Card]

    def __init__(self, playerNum:Players):
        self._cards = []
        for suit in Suit:
            for rank in Rank:
                # TODO: add pictures
                self._cards.append(Card(rank, suit, playerNum))

    @property
    def cards(self) -> list[Card]:
        return self._cards
    
    @property
    def size(self) -> int:
        return len(self._cards)

    def shuffle(self) -> None:
        shuffle(self._cards)

    def draw_n_cards(self, num_cards:int) -> list[Card]:
        picked_cards:list[Card] = []
        for _ in range(num_cards):
            picked_cards.append(self._cards.pop())
        return picked_cards
    
    def draw_remaining_cards(self) -> list[Card]:
        picked_cards:list[Card] = self._cards
        self._cards = []
        return picked_cards

        