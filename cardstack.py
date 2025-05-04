from enum import Enum

from card import Card, TransferredCard
from player import Players

class Stacks(Enum):
    """The various stacks in the game."""
    DECK:str = "Deck"
    CRAPETTE:str = "Crapette"
    REMAINDER:str = "Remainder"
    BIN:str = "Bin"
    TABLEAU_STACK:str = "Tableau Stack"
    FOUNDATION_STACK:str = "Foundation Stack"
    # The below do not contain cards, only stacks of cards
    TABLEAU:str = "Tableau"
    FOUNDATION:str = "Foundation"

class StacksInitSizes(Enum):
    """The number of cards in each stack at the start of the initialised game."""
    DECK:int = 52
    CRAPETTE: int = 13
    REMAINDER: int = 35
    BIN: int = 0
    TABLEAU_STACK: int = 1
    FOUNDATION_STACK:int = 0
    # The below do not contain cards, only stacks of cards
    TABLEAU: int = 0
    FOUNDATION: int = 0



class CardStack:
    _cards: list[Card]
    _stack_name: Stacks
    _player_num: Players
    
    
    @property
    def cards(self) -> list[Card]:
        """Return the list of cards in the Stack

        Returns:
            list[Card]: the list of cards
        """
        return self._cards
    
    @property
    def size(self) -> int:
        return len(self.cards)
    
    @property
    def what_stack_am_i(self) -> Stacks:
        return self._stack_name
    
    @property
    def top_card(self) -> Card:
        return self.cards[self.size - 1]
    
    @property
    def second_top_card(self) -> Card:
        return self.cards[self.size - 2]

    @property
    def is_empty(self) -> bool:
        return self.size == 0
    
    @property
    def is_player(self) -> Players:
        return self._player_num

    # The "can_be_added" method contains the specific stack's rules for adding a card
    # So needs to be overridden
    def can_be_added(self, transferred_card: TransferredCard) -> bool:
        print("The method 'can_be_added' has not yet been overridden, but it must be.")
        print(f"{transferred_card.card=}, {transferred_card.from_player=}, {transferred_card.from_stack_name=}, {transferred_card.from_stack_owner=}")
        return False

    def add_card(self, transferred_card: TransferredCard) -> bool:
        if self.can_be_added(transferred_card):
            self._cards.append(transferred_card.card)
            return True
        return False
     
    def force_add_card(self, card: Card) -> None:
        """Force add a card, for debug purpose

        Args:
            card (Card): The card to add
        """
        card.turn_face_up()
        self._cards.append(card)

    def remove_top_card(self) -> bool:
        """Remove the top card from the Stack

        Returns:
            bool: True if the card was removed, False if no card was removed
        """
        if self.is_empty:
            return False
        
        try:
            self._cards.pop()
        except Exception as e:
            print(f"Error {e} removing a card from the {self.what_stack_am_i} stack")
            return False
        
        if self.size > 0:
            self.top_card.turn_face_up()
            
        return True
        
    def draw_top_card(self, drawing_player: Players) -> TransferredCard | None:
        """Draw the top card from the pack (but leaves it there)
        if the pile is empty or there is a problem drawing out a card, returns None.
        The drawn card is left on the crapette stack and will need to be removed with remove_card once it has been placed on another stack

        Returns:
            Card: the top card if the card could be drawn, otherwise none
        """
        if self.is_empty:
            print(f"No card on {self.what_stack_am_i} stack")
            return None
        
        try:
            drawn_card: TransferredCard = TransferredCard(#= TransferredCard()
            from_player = drawing_player,
            from_stack_name = self.what_stack_am_i,
            from_stack_owner = self._player_num,
            card = self._cards[len(self._cards) - 1]
            # drawn_card:Card = self._cards[len(self._cards) - 1]
            # self._drawn_card = drawn_card
            )

        except Exception as e:
            print(f"error {e}: Could not draw card from {self._stack_name} stack")
            return None
        
        return drawn_card