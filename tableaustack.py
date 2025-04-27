from deck import Deck
from card import Card

class TableauStack:
    _cards: list[Card]

    def __init__(self, deck: Deck):
        self._cards = []
        first_card: Card = deck.draw_n_cards(1)[0]
        first_card.turn_face_up()
        self._cards.append(first_card)
