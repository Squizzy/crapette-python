import sys
sys.path.append('..')
sys.path.append('.')

from icecream import ic #type:ignore

from card import Card #, Rank, Suit
from deck import Deck
from player import Players

from samples import card_8H, card_9H, card_10H, card_7D, card_7S, card_8S, card_9S, card_QS
# import pytest

from tableaustack import TableauStack
# player_num: int = 1

# # A set of sample cards
# card_8H: Card = Card(rank=Rank.EIGHT, suit=Suit.HEARTS, player_num=1)
# card_9H: Card = Card(rank=Rank.NINE, suit=Suit.HEARTS, player_num=1)
# card_10H: Card = Card(rank=Rank.TEN, suit=Suit.HEARTS, player_num=1)

# card_7S: Card = Card(rank=Rank.SEVEN, suit=Suit.SPADES, player_num=1)
# card_8S: Card = Card(rank=Rank.EIGHT, suit=Suit.SPADES, player_num=1)
# card_9S: Card = Card(rank=Rank.NINE, suit=Suit.SPADES, player_num=1)

# card_7D: Card = Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS, player_num=1)

# card_QS: Card = Card(rank=Rank.QUEEN, suit=Suit.SPADES, player_num=1)

# One deck
deck: Deck = Deck(Players.PLAYER1)

# Normal initialised deck
tableau: TableauStack = TableauStack(deck, player_num=Players.PLAYER1)

# Deck initialised with some cards
tableau1: TableauStack = TableauStack(deck, player_num=Players.PLAYER1)
tableau1.remove_top_card()
tableau1.force_add_card(card_8S)
tableau1.force_add_card(card_9H)
tableau1.force_add_card(card_QS)
tableau1.force_add_card(card_9S)
tableau1.force_add_card(card_7D)
tableau1.force_add_card(card_7S)



def test_tableau_constructor():
    print()
    ic(tableau.what_stack_am_i)
    ic(tableau.top_card)

    assert tableau.what_stack_am_i == "Tableau" 
    assert not tableau.is_empty 
    assert type(tableau.top_card) is Card
    assert tableau.top_card.face_up
    

def test_size():
    assert tableau.size == 1

def test_top_card():
    assert type(tableau.top_card) is Card

def test_tableau_adder_rules():
    tableau.force_add_card(card_8H)
    assert not tableau.can_be_added(card_8S, player_num=Players.PLAYER1) # same rank, should fail
    assert not tableau.can_be_added(card_9H, player_num=Players.PLAYER1) # same suit, should fail
    assert not tableau.can_be_added(card_QS, player_num=Players.PLAYER1) # rank far away, should fail
    assert not tableau.can_be_added(card_9S, player_num=Players.PLAYER1) # rank above, should fail
    assert not tableau.can_be_added(card_7D, player_num=Players.PLAYER1) # rank below but same colour, should fail
    assert tableau.can_be_added(card_7S, player_num=Players.PLAYER1) # rank below, opposite colour, should pass

def test_add_card():
    # top card is 8H
    assert not tableau.add_card(card_7D, player_num=Players.PLAYER1)
    assert not tableau.add_card(card_9H, player_num=Players.PLAYER1)
    assert tableau.add_card(card_7S, player_num=Players.PLAYER1)
    assert tableau.top_card == card_7S

def test_remove_card() -> None:
    size1: int = tableau.size
    tableau.remove_top_card()
    assert tableau.size == size1 - 1

def test_return_position_in_cards():
    # ic(tableau1.what_stack_am_i)
    assert tableau1.position_in_stack(card_QS) != 5
    assert tableau1.position_in_stack(card_QS) == 2
    assert tableau1.position_in_stack(card_8H) is None
    print()

def test_select_cards():
    tableau1.select_cards(card_9S)
    assert tableau1.selected_cards[0] == card_9S
    assert tableau1.selected_cards[1] == card_7D
    assert tableau1.selected_cards[2] == card_7S
    assert tableau1._cards[tableau1.position_in_stack(card_9S)] == card_9S

def test_deselect():
    tableau1.deselect_cards()
    assert len(tableau1._selected_cards) == 0
    assert tableau1._cards[tableau1.position_in_stack(card_9S)] == card_9S

def test_remove_cards():
    size1 = tableau1.size
    tableau1.select_cards(card_9S)
    tableau1.remove_selected_cards_from_stack()
    assert tableau1.size != size1
    assert tableau1.size == 3

def test_add_n_cards():
    tableau1.force_add_card(card_10H)
    # ic(len(tableau1._selected_cards))
    tableau1._selected_cards[0] = card_9S
    tableau1._selected_cards[1] = card_8H
    tableau1._selected_cards[2] = card_7S
    print()
    ic(tableau1.top_card)
    ic(tableau1._selected_cards[0])
    ic(tableau1._selected_cards[1])
    ic(tableau1._selected_cards[2])
    # add_worked = tableau1.add_n_cards(tableau1._selected_cards)
    assert tableau1.add_n_cards(tableau1._selected_cards, player_num=Players.PLAYER1)
    assert tableau1.size == 7