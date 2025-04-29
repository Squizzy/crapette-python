import sys
sys.path.append('..')

# from card import Card #, Rank, Suit
# from deck import Deck
from samples import deck, card_8H, card_9H, card_10H, card_7D, card_7S, card_7H
from icecream import ic #type:ignore


from crapettestack import CrapetteStack
player_num:int = 1

crapette: CrapetteStack = CrapetteStack(deck, player_num)

def test_constructor():
    print()
    ic(crapette.what_stack_am_i)
    
    assert crapette.what_stack_am_i == "Crapette"
    assert crapette.size == 13
    assert crapette.top_card.face_up

def test_can_be_added():
    force_add_card_to_crapette()
    assert crapette.top_card == card_8H
    assert crapette.size == 14
    assert crapette.can_be_added(card_9H)
    assert crapette.can_be_added(card_7H)
    assert not crapette.can_be_added(card_7D)
    assert not crapette.can_be_added(card_10H)
    assert not crapette.can_be_added(card_7S)
    

def test_add_card():
    assert crapette.top_card == card_8H
    assert crapette.size == 14
    crapette.add_card(card_9H)
    assert crapette.top_card == card_9H
    assert crapette.size == 15
    crapette.add_card(card_7D)


def force_add_card_to_crapette():
    crapette._cards.append(card_8H)
    crapette.top_card.turn_face_up()