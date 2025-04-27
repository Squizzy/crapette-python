import sys
sys.path.append('..')

from card import Card, Rank, Suit
from deck import Deck
from tableaustack import TableauStack
from icecream import ic
import pytest

deck = Deck(1)
tableau = TableauStack(deck)

card_8H = Card(rank=Rank.EIGHT, suit=Suit.HEARTS, player_num=1)
card_9H = Card(rank=Rank.NINE, suit=Suit.HEARTS, player_num=1)
card_10H = Card(rank=Rank.TEN, suit=Suit.HEARTS, player_num=1)

card_7S = Card(rank=Rank.SEVEN, suit=Suit.SPADES, player_num=1)
card_8S = Card(rank=Rank.EIGHT, suit=Suit.SPADES, player_num=1)
card_9S = Card(rank=Rank.NINE, suit=Suit.SPADES, player_num=1)

card_7D = Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS, player_num=1)

card_QS = Card(rank=Rank.QUEEN, suit=Suit.SPADES, player_num=1)


def test_tableau_initialisation():
    assert tableau.is_empty == False
    assert type(tableau._cards[0]) == Card


def test_size():
    assert tableau.size == 1


def test_top_card():
    assert type(tableau.top_card) == Card


def test_tableau_adder_rules():
    tableau.force_add_card(card_8H)
    assert tableau.can_be_added(card_8S) == False # same rank, should fail
    assert tableau.can_be_added(card_9H) == False # same suit, should fail
    assert tableau.can_be_added(card_QS) == False # rank far away, should fail
    assert tableau.can_be_added(card_9S) == False # rank above, should fail
    assert tableau.can_be_added(card_7D) == False # rank below but same colour, should fail
    assert tableau.can_be_added(card_7S) == True # rank below, opposite colour, should pass


def test_add_card():
    assert tableau.add_card(card_7D) == False
    assert tableau.add_card(card_9H) == False
    assert tableau.add_card(card_7S) == True
    assert tableau.top_card == card_7S


def test_remove_card():
    size1:int = tableau.size
    tableau.remove_card()
    assert tableau.size == size1 - 1


tableau1 = []
tableau1 = TableauStack(deck)
tableau1.remove_card()
tableau1.force_add_card(card_8S)
tableau1.force_add_card(card_9H)
tableau1.force_add_card(card_QS)
tableau1.force_add_card(card_9S)
tableau1.force_add_card(card_7D)
tableau1.force_add_card(card_7S)

def test_return_position_in_cards():
    assert tableau1.position_in_stack(card_QS) != 5
    assert tableau1.position_in_stack(card_QS) == 2
    assert tableau1.position_in_stack(card_8H) == None
    print()


def test_select_cards():
    
    tableau1.select_cards(card_9S)
    assert tableau1._selected_cards[0] == card_9S
    assert tableau1._selected_cards[1] == card_7D
    assert tableau1._selected_cards[2] == card_7S
    assert tableau1._cards[tableau1.position_in_stack(card_9S)] == card_9S
    # selected_cards: list[Card]|None = tableau1.select_cards(card_9S)
    # assert selected_cards[0] == card_9S
    # assert selected_cards[1] == card_7D
    # assert selected_cards[2] == card_7S
    # assert tableau1._cards[tableau1.position_in_stack(card_9S)] == card_9S


def test_deselect():
    tableau1.deselect_cards()
    assert len(tableau1._selected_cards) == 0
    assert tableau1._cards[tableau1.position_in_stack(card_9S)] == card_9S


def test_remove_cards():
    size1 = tableau1.size
    tableau1.select_cards(card_9S)
    tableau1.remove_selected_cards()
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
    assert tableau1.add_n_cards(tableau1._selected_cards) == True
    assert tableau1.size == 7