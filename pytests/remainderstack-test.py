import sys
sys.path.append('..')

from card import Card #, Rank, Suit
from deck import Deck
from icecream import ic
from remainderstack import RemainderStack
from samples import random_stacked_cards

deck = Deck(1)
remainder = RemainderStack(deck)

def test_constructor():
    print ()
    ic(remainder._stackname)
    
    assert remainder.size == 52
    ic(remainder.top_card)

def test_draw_top_card():
    card: Card|None = remainder.draw_top_card()
    assert card == remainder.top_card
    
    tempStack: list[Card] = remainder._cards
    remainder._cards  = []
    card = remainder.draw_top_card()
    assert not card # card is None
    remainder._cards = tempStack

def test_reload_from_binstack():
    binstack_cards = random_stacked_cards
    # When remainderstack still has some cards, this should return False
    assert remainder.size == 52
    # assert remainder.top_card == card_7S
    # assert remainder._cards[0] == card_7S
    # assert remainder._cards[1] == card_8S
    # assert remainder._cards[2] == card_9S
    # assert remainder._cards[3] == card_QS
    # assert remainder._cards[4] == card_9S
    # assert remainder._cards[5] == card_7D
    # assert remainder._cards[6] == card_7S
    # assert remainder._cards[7] == card_8S
    # assert remainder._cards[8] == card_9S
    # assert remainder._cards[9] == card_QS
    # assert remainder._cards[10] == card_9S
    # assert remainder._cards[11] == card_7D
    # assert remainder._cards[12] == card_7
    assert not remainder.reload_from_binstack(binstack_cards)
    
    tempstack = remainder._cards
    remainder._cards = []
    assert remainder.reload_from_binstack(binstack_cards)
    remainder._cards = tempstack