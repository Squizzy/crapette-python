from enum import Enum
from stacks import Stacks
from constants import Players

# the enum representing the card suits
class Suit(Enum):
    CLUBS = "Clubs"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    SPADES = "Spades"
    
    @property
    def colour(self) -> str:
        if self in (Suit.HEARTS, Suit.DIAMONDS):
            return "red"
        return "black"
    
    @property
    def short(self) -> str:
        return self.value[0]
    
# the enum representing the card values
class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13    

    @property
    def display_name(self) -> str:
        if self == Rank.ACE:
            return "Ace"
        elif self.value >= 2 and self.value <= 10:
            return str(self.value)
        elif self == Rank.JACK:
            return "Jack"
        elif self == Rank.QUEEN:
            return "Queen"
        elif self == Rank.KING:
            return "King"
        return str(self.value)
    
    @property
    def short(self) -> str:
        return str(self.value if self.value  <= 10 else "J" if self.value == 11 else "Q" if self.value == 12 else "K")


# The class representing the card object
class Card:
    _rank: Rank
    _suit: Suit
    _player_num: Players
    _face_up: bool



    def __init__(self, rank:Rank, suit:Suit, player_num:Players, face_img:str = "", back_img:str = "", face_up:bool = False):
        self._rank =  rank
        self._suit = suit
        self._face_img = face_img
        self._back_img = back_img
        self._face_up = face_up
        self._player_num = player_num

    def __repr__(self) -> str:
        face_status:str = "face up" if self.face_up else "face down"
        return f"{self.rank} of {self.suit} - {face_status}"

    def __str__(self) -> str:
        return self._suit.short + self._rank.short +  ('u' if self._face_up else 'd') + str(self._player_num.value)

    def to_dict(self) -> dict:
        # TODO: Check if still needed
        # return the card detail in dictionary format to be JSON serialisable
        # return self._rank.short + self._suit.short + ('u' if self._face_up else 'd')
        return {
            "value": self._rank.short + self._suit.short + ('u' if self._face_up else 'd'),
        }
        
    @property
    def rank(self) -> str:
        return self._rank.display_name
    
    @property
    def value(self) -> int:
        return self._rank.value
    
    @property
    def suit(self) -> str:
        return self._suit.value
    
    @property
    def colour(self) -> str:
        return self._suit.colour
    
    @property
    def face_up(self) -> bool:
        return self._face_up

    @property
    def card_short(self) -> str:
        return str(self.suit[0] + str(self.rank)+ ('u' if self.face_up else 'd'))

    def flip_card(self):
        self._face_up = not self._face_up

    def turn_face_up(self):
        self._face_up = True

    def turn_face_down(self):
        self._face_up = False
   
    def is_same_colour(self, card: "Card") -> bool:
        return card.colour == self.colour
    
    def is_same_family(self, card:"Card") -> bool:
        return card.suit == self.suit
    
    def is_one_above(self, card: "Card") -> bool:
        return card.value == self.value - 1
    
    def is_one_below(self, card: "Card") -> bool:
        return card.value == self._rank.value + 1
    
    def is_one_above_or_below(self, card: "Card") -> bool:
        return self.is_one_above(card) or self.is_one_below(card)
    
class TransferredCard:
    _from_player: Players
    _from_stack_name: Stacks
    _from_stack_owner: Players
    _card: Card

    def __init__(self, from_player: Players, from_stack_name: Stacks, from_stack_owner: Players, card: Card):
        self._from_player = from_player
        self._from_stack_name = from_stack_name
        self._from_stack_owner = from_stack_owner
        self._card = card
        
    def __repr__(self):
        return f"{self.card.rank} of {self.card.suit} - from {self.from_player} - {self.from_stack_name} owned by {self.from_stack_owner}"
    
    @property
    def from_player(self) -> Players:
        return self._from_player
    
    @property
    def from_stack_name(self) -> Stacks:
        return self._from_stack_name
    
    @property
    def from_stack_owner(self) -> Players:
        return self._from_stack_owner
    
    @property
    def card(self) -> Card:
        return self._card

class TransferredNCards:
    _transferred_cards: list[TransferredCard]
    # _from_player: Players
    # _from_stack_name: Stacks
    # _from_stack_owner: Players
    # _cards: list[Card]
    
    def __init__(self, from_player: Players, from_stack_name: Stacks, from_stack_owner: Players, cards: list[Card]):
        if from_stack_name != Stacks.TABLEAU_STACK:
            raise ValueError("Error: Transferred_N_Cards can only be created from the Tableau stack")
        
        if len(cards) == 0:
            raise ValueError("Error: Transferred_N_Cards must contain at least one card")
        
        self._transferred_cards = []  # create the empty stack of cards
        for card in cards:
            transferred_card: TransferredCard = TransferredCard(from_player=from_player, 
                                                                from_stack_name=from_stack_name, 
                                                                from_stack_owner=from_stack_owner, 
                                                                card=card)
            self._transferred_cards.append(transferred_card)
        
    def __repr__(self) -> str:
        return f"{self.size} cards starting with {self.bottom_card.card.rank} of {self.bottom_card.card.suit} - from {self.from_player} - {self.from_stack_name} owned by {self.from_stack_owner}"
    
    @property
    def size(self) -> int:
        return len(self._transferred_cards)
    
    @property
    def from_stack_name(self) -> Stacks:
        return self._transferred_cards[0]._from_stack_name
    
    @property
    def from_stack_owner(self) -> Players:
        return self._transferred_cards[0]._from_stack_owner
    
    @property
    def transferred_cards(self) -> list[TransferredCard]:
        return self._transferred_cards
    
    @property
    def cards(self) -> list[Card]:
        return [transferred_card.card for transferred_card in self._transferred_cards]
    
    @property
    def bottom_card(self) -> TransferredCard:
        return self._transferred_cards[0]
    
    @property
    def from_player(self) -> Players:
        return self._transferred_cards[0]._from_player    
    
    # @property
    # def top_card(self) -> Card:
    #     return self._transferred_cards[self.size -1]

