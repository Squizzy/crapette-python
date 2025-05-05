import sys
sys.path.append('..')
sys.path.append('.')

from card import Card, TransferredCard #, Rank, Suit, 
from deck import Deck
from stacks import Stacks
from samples import random_stacked_cards
from player import Players
from icecream import ic #type:ignore

from remainderstack import RemainderStack

# One deck
deck: Deck = Deck(Players.PLAYER1)

# ic(deck.size)

deck.draw_n_cards(13) # remove the crapette cards that won't be distributed before this test here
deck.draw_n_cards(4) # remove the Tableau cards that won't be distributed before this test here

remainder = RemainderStack(deck, Players.PLAYER1)

def test_constructor():
    print ()
    ic(remainder.what_stack_am_i)
    ic(remainder.top_card)

    assert remainder.what_stack_am_i == Stacks.REMAINDER
    assert remainder.size == 52 - 13 - 4
    assert not remainder.top_card.face_up
    
    
def test_draw_top_card() -> None:
    # card: Card|None = remainder.draw_top_card()
    drawn_card: TransferredCard|None = remainder.draw_top_card(Players.PLAYER1)
    assert drawn_card is not None
    assert drawn_card.card == remainder.top_card
    
    tempStack: list[Card] = remainder._cards
    remainder._cards  = []
    card = remainder.draw_top_card(Players.PLAYER1)
    assert not card # card is None
    remainder._cards = tempStack

def test_reload_from_binstack():
    binstack_cards = random_stacked_cards
    
    # When remainderstack still has some cards, this should return False
    assert remainder.size == 52 - 13 - 4
    assert not remainder.reload_from_binstack(binstack_cards)
    
    # When the stack is empty, binstack content can be added 
    tempstack = remainder._cards
    remainder._cards = []
    assert remainder.reload_from_binstack(binstack_cards)
    assert len(remainder._cards) == len(binstack_cards)
    remainder._cards = tempstack
    assert len(remainder._cards) == 52 - 13 - 4