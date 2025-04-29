from card import Card, Rank, Suit
from deck import Deck
from tableaustack import TableauStack

# A set of sample cards
#red
card_7H: Card = Card(rank=Rank.SEVEN, suit=Suit.HEARTS, player_num=1)
card_8H: Card = Card(rank=Rank.EIGHT, suit=Suit.HEARTS, player_num=1)
card_9H: Card = Card(rank=Rank.NINE, suit=Suit.HEARTS, player_num=1)
card_10H: Card = Card(rank=Rank.TEN, suit=Suit.HEARTS, player_num=1)

card_7D: Card = Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS, player_num=1)
card_QD: Card = Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS, player_num=1)

# black
card_7S: Card = Card(rank=Rank.SEVEN, suit=Suit.SPADES, player_num=1)
card_8S: Card = Card(rank=Rank.EIGHT, suit=Suit.SPADES, player_num=1)
card_9S: Card = Card(rank=Rank.NINE, suit=Suit.SPADES, player_num=1)

card_JS: Card = Card(rank=Rank.JACK, suit=Suit.SPADES, player_num=1)
card_QS: Card = Card(rank=Rank.QUEEN, suit=Suit.SPADES, player_num=1)

random_stacked_cards: list[Card] = [card_7S, card_8S, card_9S, card_QS, card_9S, card_7D, card_7S]
correct_stacked_cards_down_low: list[Card]   = [card_7S, card_8H, card_9S]
correct_stacked_cards_down_high: list[Card]  = [card_10H, card_JS]

# One deck
deck: Deck = Deck(1)

# Normal initialised deck
tableau: TableauStack = TableauStack(deck, 1)

# Deci initialised with some cards
tableau1: TableauStack = TableauStack(deck, 1)
tableau1.remove_top_card()
tableau1.force_add_card(card_8S)
tableau1.force_add_card(card_9H)
tableau1.force_add_card(card_QS)
tableau1.force_add_card(card_9S)
tableau1.force_add_card(card_7D)
tableau1.force_add_card(card_7S)
