import sys
sys.path.append('..')

from card import Card, Rank, Suit
from deck import Deck
from icecream import ic
from remainderstack import RemainderStack

deck = Deck(1)
remainder = RemainderStack(deck)

def test_constructor():
    assert remainder.size == 52
    print ()
    ic(remainder.top_card)

def test_draw_card():
    card = remainder.