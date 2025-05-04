import sys
sys.path.append('..')
sys.path.append('.')
# from icecream import ic #type:ignore


from card import Card, Rank, Suit
from player import Players
# import pytest

card_7S = Card(rank=Rank.SEVEN, suit=Suit.SPADES, player_num=Players.PLAYER1)
card_8H = Card(rank=Rank.EIGHT, suit=Suit.HEARTS, player_num=Players.PLAYER1)
card_9S = Card(rank=Rank.NINE, suit=Suit.SPADES, player_num=Players.PLAYER1)
card_QS = Card(rank=Rank.QUEEN, suit=Suit.SPADES, player_num=Players.PLAYER1)



def test_card_generation():
    card_KC = Card(rank=Rank.KING, suit=Suit.CLUBS, player_num=Players.PLAYER1)
    assert card_KC._rank == Rank.KING
    assert card_KC._suit == Suit.CLUBS
    assert not card_KC._face_up
    assert card_KC._back_img == ""
    assert card_KC._face_img == ""
    assert card_KC._player_num == Players.PLAYER1


def test_rank():
    assert card_8H.rank == '8'
    assert card_QS.rank == 'Queen'
    

def test_suit():
    assert card_8H.suit == 'Hearts'
    assert card_QS.suit == 'Spades'
    assert card_QS.suit != 'clubs'


def test_repr():
    assert str(card_QS) == 'Queen of Spades - face down'


def test_face_up():
    assert not card_8H.face_up
    card_8H.flip_card()
    assert card_8H.face_up
    card_8H.flip_card()
    assert not card_8H.face_up


def test_turn_face_up():
    assert not card_8H.face_up
    card_8H.turn_face_up()
    assert card_8H.face_up
    card_8H.turn_face_up()
    assert card_8H.face_up


def test_turn_face_down():
    assert card_8H.face_up
    card_8H.turn_face_down()
    assert not card_8H.face_up
    card_8H.turn_face_down()
    assert not card_8H.face_up
    
def test_is_one_above():
    # ic(card_8H.rank)
    # ic(card_8H._rank.value)
    # ic(card_7S._rank.value)
    # ic(card_QS._rank.value)
    # ic(card_QS.rank)
    assert card_8H.is_one_above(card_7S)
    assert card_8H.is_one_below(card_9S)
    