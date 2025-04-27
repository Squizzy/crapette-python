from enum import Enum

class Suit(Enum):
    CLUBS = "Clubs"
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    SPADES = "Spades"
    
    @property
    def color(self) -> str:
        if self in (Suit.HEARTS, Suit.DIAMONDS):
            return "red"
        return "black"
    
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

class Card:
    _rank: Rank
    _suit: Suit
    _player_num: int
    #TODO: Work out how to do images
    _face_img: str
    _back_img: str
    _face_up: bool


    def __init__(self, rank:Rank, suit:Suit, player_num:int, face_img:str = "", back_img:str = "", face_up:bool = False):
        self._rank =  rank
        self._suit = suit
        self._face_img = face_img
        self._back_img = back_img
        self._face_up = face_up
        self._player_num = player_num

    def __repr__(self) -> str:
        face_status:str = "face up" if self._face_up else "face down"
        return f"{self._rank.display_name} of {self._suit.value} - {face_status}"

    @property
    def value(self) -> str:
        return self.values[self._rank.display_name]
    
    @property
    def suit(self) -> str:
        return self._suit.value
    
    @property
    def face_up(self) -> bool:
        return self._face_up

    def flip_card(self):
        self._face_up = not self._face_up

    def turn_face_up(self):
        self._face_up = True

    def turn_face_down(self):
        self._face_up = False
   
    def is_same_colour(self, card: "Card") -> bool:
        return card._suit.color == self._suit.color
    
    def is_same_family(self, card:"Card") -> bool:
        return card._suit == self._suit
    
    def is_one_above(self, card: "Card") -> bool:
        return card._rank.value == self._rank.value + 1
    
    def is_one_below(self, card: "Card") -> bool:
        return card._rank.value == self._rank.value - 1
    
    def is_one_above_or_below(self, card: "Card") -> bool:
        return self.is_one_above(card) or self.is_one_below(card)