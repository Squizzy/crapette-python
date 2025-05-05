import sys
sys.path.append('..')
sys.path.append('.')

from icecream import ic #type:ignore

# from card import Card #, Rank, Suit
from deck import Deck
from player import Players
from stacks import Stacks
from crapettestack import CrapetteStack

from samples import card_7H, card_8H, card_9H, card_10H
from samples import card_7D
from samples import card_7S
from samples import card_7H_transferred_1c1, card_7H_transferred_1c2, card_7H_transferred_2c1, card_7H_transferred_1t1, card_7H_transferred_2t1
from samples import card_9H_transferred_1c1, card_10H_transferred_1c1
from samples import card_7D_transferred_1c1
from samples import card_7S_transferred_1c1


# One deck - reset the deck size as 2 cards were taken for the tableaux above
deck: Deck = Deck(Players.PLAYER1)

crapette: CrapetteStack = CrapetteStack(deck, Players.PLAYER1)

def test_constructor():
    print()
    ic(crapette.what_stack_am_i)
    ic(crapette.top_card)
    
    assert crapette.what_stack_am_i == Stacks.CRAPETTE
    assert crapette.size == 13
    assert crapette.top_card.face_up

def test_can_be_added():
    force_add_card_to_crapette()
    assert crapette.top_card == card_8H
    assert crapette.size == 14
    assert crapette.can_be_added(card_9H_transferred_1c1)
    assert crapette.can_be_added(card_7H_transferred_1c1)
    assert not crapette.can_be_added(card_7D_transferred_1c1)
    assert not crapette.can_be_added(card_10H_transferred_1c1)
    assert not crapette.can_be_added(card_7S_transferred_1c1)
    

def test_add_card():
    assert crapette.top_card == card_8H
    assert crapette.size == 14
    crapette.add_card(card_7H_transferred_1c1) # should work
    assert crapette.top_card == card_7H ##
    assert crapette.size == 15
    crapette.add_card(card_7D_transferred_1c1)


def force_add_card_to_crapette():
    crapette._cards.append(card_8H)
    crapette.top_card.turn_face_up()