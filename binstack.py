from card import Card, TransferredCard, TransferredNCards
from cardstack import CardStack
from stacks import Stacks, StacksInitSizes
from player import Players
from gamestates import PlayersGameState, GameStates

# The class representing the player's bin object

class BinStack(CardStack):
    _stack_name: Stacks
    _cards: list[Card]
    _player_num: Players
    
    def __init__(self, player_num: Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Bin stack - player specified incorrect: {player_num}")
        self._stack_name = Stacks.BIN  # Name of the stack
        self._player_num = player_num  # Player number of the stack owner
        self._cards = []  # create the empty stack of cards
        if len(self._cards) != StacksInitSizes.BIN.value:  # check the number of cards in the stack
            raise ValueError(f"Error: The {self.what_stack_am_i} deck should have {StacksInitSizes.BIN.value} cards, but it has {self.size} cards")
        PlayersGameState.set_player_flag(player_num = player_num, flag = GameStates.Player.BIN_IS_EMPTY)  # set the player state for the player who owns the stack
        
    def can_be_added(self, transferred_card: TransferredCard) -> bool:
        """The bin can receive one card at a time, from the current and from the other player:
         player: Any card as long as it comes from the current player's remainder stack
         opponent: card must be other color than top card, of value +/1, and 
         must be either from the opponent's crapette, remainder, or from any of the tableaux stack
        """
        
        if transferred_card.from_player == self.is_player:
            if transferred_card.from_stack_name == Stacks.REMAINDER:
                if transferred_card.from_stack_owner == self.is_player:
                    return True
            else:
                return False
                
        else:
            if transferred_card.card.is_same_colour(self.top_card) or \
                not transferred_card.card.is_one_above_or_below(self.top_card):
                return False
            
            if transferred_card.from_stack_name in [Stacks.CRAPETTE, Stacks.REMAINDER]:
                if transferred_card.from_stack_owner ==  Players.PLAYER1 if self.is_player == Players.PLAYER2 else Players.PLAYER2:
                    return True
            
            if transferred_card.from_stack_name == Stacks.TABLEAU_STACK:
                return True
            
        return False

    def bincards_for_reminder_stack(self) -> TransferredNCards | None:
        """Returns all the cards in the bin stack as transferredNCards
        This does not modify the bin stack content

        Returns:
            TransferredNCards | None: The list of cards, or None if no card
        """
        if self.is_empty:
            return None
        
        bincards: TransferredNCards = TransferredNCards(
                from_player = self.is_player,
                from_stack_name = Stacks.BIN,
                from_stack_owner = self.is_player,
                cards = self.cards
            )
        return bincards
    
    def empty_bin(self) -> bool:
        """Empties the bin stack and reset appropriate flags
        the flag indicting that the bin is now empty
        the flag indicating that the remainder bin had just retrieved the bin cards so the bin cards could be removed

        Returns:
            bool: currently just returns True, might not be needed.
        """
        if self.is_empty:
            return True

        self._cards = []
        # As this is effected when the players moved his bin cards to remainder, we can reset this flag
        PlayersGameState.clear_player_flag(self.is_player, flag = GameStates.Player.PLAYER_MOVED_BIN_CARDS_TO_REMAINDER)
        PlayersGameState.set_player_flag(self.is_player, flag = GameStates.Player.BIN_IS_EMPTY)  # set the player state for the player who owns the stack
        return True