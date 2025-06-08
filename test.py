# from card import Card, Rank, Suit
from deck import Deck
# from crapettestack import CrapetteStack
from stacks_tableau import TableauStacks
from player import Players
# from samples import deck

deck = Deck(Players.PLAYER1)

# player_num = 1

# card1: Card = Card(rank=Rank.FIVE, suit=Suit.CLUBS, player_num=Players.PLAYER1)
# card2: Card = Card(rank=Rank.SIX, suit=Suit.CLUBS, player_num=Players.PLAYER1)
# card3: Card = Card(rank=Rank.FIVE, suit=Suit.HEARTS, player_num=Players.PLAYER1)
# card4: Card = Card(rank=Rank.FOUR, suit=Suit.CLUBS, player_num=Players.PLAYER1)

# p1deck:Deck = Deck(Players.PLAYER1)
# p1deck.shuffle()
# # p1deck_cards = p1deck.list_cards()
# # for card in p1deck_cards:
# #     print(f"{card.value()} of {card.suit()}")
# p1crapette:CrapetteStack = CrapetteStack(p1deck, Players.PLAYER1)
# p1crapette_cards = p1crapette.cards
# for card in p1crapette_cards:
#     # print(f"{card._rank.display_name} of {card.suit()} - {card.face_up()}")
#     print(f"{card}")
# print("###")
# crapette_card = p1crapette.draw_top_card(Players.PLAYER1)
# # print(f"{crapette_card.value()} of {crapette_card.suit()} - {crapette_card.face_up()}")
# print("###")
# # for card in p1crapette_cards:
# #     print(f"{card.value()} of {card.suit()} - {card.face_up()}")
# # print("###")
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# p1crapette.remove_top_card()
# for card in p1crapette_cards:
#     print(card)

# print("### - Add card1")
# p1crapette.force_add_card(card1)
# for card in p1crapette_cards:
#     print(card)

# print("### - Add card2")
# p1crapette.add_card(card2, Players.PLAYER1)
# for card in p1crapette_cards:
#     print(card)

# print("### - Remove Card 2")
# p1crapette.remove_top_card()
# for card in p1crapette_cards:
#     print(card)

# print("### - Add card3")
# p1crapette.add_card(card3, Players.PLAYER1)
# for card in p1crapette_cards:
#     print(card)

# print("### - Add card4")
# p1crapette.add_card(card4, Players.PLAYER1)
# for card in p1crapette_cards:
#     print(card)

# print("### - Create Tableau")
# tableau: TableauStacks = TableauStacks(p1deck, Players.PLAYER1)
# print(tableau._TableauStacks[0]._cards[0])
# print(tableau._TableauStacks[1]._cards[0])
# print(tableau._TableauStacks[2]._cards[0])
# print(tableau._TableauStacks[3]._cards[0])

# tableau = TableauStacks(deck, Players.CARDSTACK)