from stacks import Stacks
from card import Card, TransferredCard
from constants import Players
from server_game_state import GameStates, PlayersGameState
from abc import ABC, abstractmethod

# Generic stack class from which all the stacks that hold cards inherit.

class CardStack(ABC):
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
    
    def to_list(self) -> list[str]:
        return [str(card) for card in self._cards]
    
    def to_dict(self) -> dict[str, str | list[dict[str,str]]]:
        """Return the stack as a dictionary."""
        # return [card.to_dict() for card in self._cards]
        return {
            "stack_name": self._stack_name.value,
            "cards": [card.to_dict() for card in self._cards]
        }
    
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
    @abstractmethod
    def can_be_added(self, transferred_card: TransferredCard) -> bool:
        print("The method 'can_be_added' has not yet been overridden, but it must be.")
        print(f"{transferred_card.card=}, {transferred_card.from_player=}, {transferred_card.from_stack_name=}, {transferred_card.from_stack_owner=}")
        return False

    def add_card(self, transferred_card: TransferredCard) -> bool:
        """Add a card to the Stack, if the Stack allows it.

        Args:
            transferred_card (TransferredCard): The card to be added

        Returns:
            bool: True if the card was added, False if it was not
        """        
        if self.can_be_added(transferred_card):
            self._cards.append(transferred_card.card)
            return True
        return False
     
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
        
        # No player can draw fromm a bin or foundation stack
        if self.what_stack_am_i in [Stacks.BIN, Stacks.FOUNDATION_STACK]:
            return None
        
        # Only the owner can draw from his own crapette or remainder stack
        if self.what_stack_am_i in [Stacks.CRAPETTE, Stacks.REMAINDER]:
            if drawing_player != self.is_player:
                return None
        
        try:
            # create the transferred card
            drawn_card: TransferredCard = TransferredCard(#= TransferredCard()
            from_player = drawing_player,
            from_stack_name = self.what_stack_am_i,
            from_stack_owner = self._player_num,
            card = self._cards[len(self._cards) - 1]
            )
            
            # Always turn a card picked face up
            drawn_card.card.turn_face_up()  

        except Exception as e:
            print(f"error {e}: Could not draw card from {self._stack_name} stack")
            return None
        
        return drawn_card
    
    def remove_top_card(self) -> bool:
        """Remove (delete) the top card from the Stack

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
            
        if self.size == 0:
            flag: GameStates.Player
            match self.what_stack_am_i:
                case Stacks.CRAPETTE:
                    flag = GameStates.Player.CRAPETTE_IS_EMPTY
                case Stacks.REMAINDER:
                    flag = GameStates.Player.REMAINDER_IS_EMPTY
                # NOTE: It is not possible to pick from the bin so this is not set here
                # TODO: Add Tableau and Foundation stacks if needed
                case _:
                    pass
            if flag in [GameStates.Player.CRAPETTE_IS_EMPTY, GameStates.Player.REMAINDER_IS_EMPTY]:
                PlayersGameState.set_player_flag(self.is_player, flag)
            
        return True
    
    # FOR DEBUG PURPOSE ONLY:    
    def force_add_card(self, card: Card) -> None:
        """Force add a card, for debug purpose

        Args:
            card (Card): The card to add
        """
        card.turn_face_up()
        self._cards.append(card)

