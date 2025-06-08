from card import Card, Rank, Suit, TransferredCard, TransferredNCards
from stacks import Stacks
from deck import Deck
from stack_tableau import TableauStack
from player import Players

# A set of sample cards
#red
card_7H: Card = Card(rank=Rank.SEVEN, suit=Suit.HEARTS, player_num=Players.PLAYER1)
card_8H: Card = Card(rank=Rank.EIGHT, suit=Suit.HEARTS, player_num=Players.PLAYER1)
card_9H: Card = Card(rank=Rank.NINE, suit=Suit.HEARTS, player_num=Players.PLAYER1)
card_10H: Card = Card(rank=Rank.TEN, suit=Suit.HEARTS, player_num=Players.PLAYER1)

card_7D: Card = Card(rank=Rank.SEVEN, suit=Suit.DIAMONDS, player_num=Players.PLAYER1)
card_QD: Card = Card(rank=Rank.QUEEN, suit=Suit.DIAMONDS, player_num=Players.PLAYER1)

# black
card_7S: Card = Card(rank=Rank.SEVEN, suit=Suit.SPADES, player_num=Players.PLAYER1)
card_8S: Card = Card(rank=Rank.EIGHT, suit=Suit.SPADES, player_num=Players.PLAYER1)
card_9S: Card = Card(rank=Rank.NINE, suit=Suit.SPADES, player_num=Players.PLAYER1)

card_JS: Card = Card(rank=Rank.JACK, suit=Suit.SPADES, player_num=Players.PLAYER1)
card_QS: Card = Card(rank=Rank.QUEEN, suit=Suit.SPADES, player_num=Players.PLAYER1)

random_stacked_cards: list[Card] = [card_7S, card_8S, card_9S, card_QS, card_9S, card_7D, card_7S]
correct_stacked_cards_down_low: list[Card]   = [card_7S, card_8H, card_9S]
correct_stacked_cards_down_high: list[Card]  = [card_10H, card_JS]

# A set of sample Transferred_Card
card_7H_transferred_1t1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, card=card_7H)
card_7H_transferred_2t1: TransferredCard = TransferredCard(from_player=Players.PLAYER2, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, card=card_7H)
card_7H_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_7H)
card_7H_transferred_1c2: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER2, card=card_7H)
card_7H_transferred_2c1: TransferredCard = TransferredCard(from_player=Players.PLAYER2, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_7H)

card_8H_transferred_1t1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, card=card_8H)
card_9H_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_9H)
card_10H_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_10H)

card_7D_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_7D)

card_7S_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_7S)
card_7S_transferred_1t1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, card=card_7S)
card_8S_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_8S)
card_9S_transferred_1t1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, card=card_9S)
card_QS_transferred_1c1: TransferredCard = TransferredCard(from_player=Players.PLAYER1, from_stack_name=Stacks.CRAPETTE, from_stack_owner=Players.PLAYER1, card=card_QS)

# A set of sample TransferredNCards
transferredNCards_9S_8H_7S: TransferredNCards = TransferredNCards(from_player=Players.PLAYER1, from_stack_name=Stacks.TABLEAU_STACK, from_stack_owner=Players.PLAYER1, cards=[card_9S, card_8H, card_7S])

# One deck
tableaux_deck: Deck = Deck(playerNum=Players.PLAYER1)

# Normal initialised deck
tableau: TableauStack = TableauStack(tableaux_deck, Players.PLAYER1)

# Deci initialised with some cards
tableau1: TableauStack = TableauStack(tableaux_deck, Players.PLAYER1)
tableau1.remove_top_card()
tableau1.force_add_card(card_8S)
tableau1.force_add_card(card_9H)
tableau1.force_add_card(card_QS)
tableau1.force_add_card(card_9S)
tableau1.force_add_card(card_7D)
tableau1.force_add_card(card_7S)


