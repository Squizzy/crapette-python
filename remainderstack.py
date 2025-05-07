from cardstack import CardStack
from stacks import Stacks, StacksInitSizes
from player import Players
from card import Card, TransferredCard, TransferredNCards
from deck import Deck
from gamestates import GameStates, PlayersGameState

# The class representiing the player's remainder stack object

class RemainderStack(CardStack):
    _stack_name: Stacks
    _cards: list[Card]
    _player_num: Players

    def __init__(self, deck: Deck, player_num: Players):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Remainder stack - player specified incorrect: {player_num}")
        self._stack_name = Stacks.REMAINDER  # Name of the stack
        self._player_num = player_num  # Player number of the stack owner
        self._cards = []  # create the empty stack of cards
        self._cards = deck.draw_remaining_cards()  # draw the remaining cards from the deck
        if len(self._cards) != StacksInitSizes.REMAINDER.value:  # check the number of cards in the stack
            raise ValueError(f"Error: The {self.what_stack_am_i} deck should have {StacksInitSizes.REMAINDER.value} cards, but it has {self.size} cards")
        PlayersGameState.clear_player_flag(player_num = player_num, flag = GameStates.Player.REMAINDER_IS_EMPTY)  # set the player state for the player who owns the stack
    
    def reload_from_binstack(self, binstack_cards: TransferredNCards) -> bool:
        """Reloads the Remainder stack from the Bin stack.
        This method should only be called when the Bin stack is empty.
        The cards are added to the Remainder stack in reverse order, and they are turned face down.
        This method does not empty the Bin stack
        
        Args:
            binstack_cards (TransferredNCards): The list of cards to be added to the Remainder stack
            
        Returns:
            bool: True if the cards were added, False if the stack was not empty
        """
        if self.size != 0:
            return False
        
        
        try:
            for card in reversed(binstack_cards.cards):
                card.turn_face_down()
                self._cards.append(card)
            
        # set the flag indicating the remainder stack  no longer empty, it it isn't
            if self.size != 0:
                PlayersGameState.clear_player_flag(self.is_player, flag = GameStates.Player.REMAINDER_IS_EMPTY)  # set the player state for the player who owns the stack
            
            # set the flag indicating that the bin cards need to be purged as the transfer happened
            if binstack_cards.size == self.size:
                PlayersGameState.set_player_flag(self.is_player, flag = GameStates.Player.PLAYER_MOVED_BIN_CARDS_TO_REMAINDER)  # set the player state for the player who owns the stack
            
            return True
        
        except Exception as e:
            raise ValueError(f"Error {e} Transfer bin cards to remainder, not the same amount of cards were added to remainder as were received from the bin")
        
        
    
    def can_be_added(self, transferred_card: TransferredCard) -> bool:
        """The remainder stack can only receive cards at initialisation and when refilling from the binstack
        A player cannot add cards to it.
        This stack cannot make use of the "add_card" or "add_n_cards" methods

        Args:
            transferred_card (TransferredCard): the card proposed to be added

        Returns:
            bool: False
        """
        return False
    
    def add_card(self, transferred_card: TransferredCard) -> bool:
        """The remainder stack can only receive cards at initialisation and when refilling from the binstack
        A player cannot add cards to it.
        If a player has lifted a card, and cancels, then this card goes to the bin stack.
        Otherwise, the addition returns null

        Args:
            transferred_card (TransferredCard): the card proposed to be added

        Returns:
            bool: True if can comes from this stack AND HAS BEEN PLACED ON THE BIN, otherwise false
        """
        
        # If player puts his remainder card on the remainder deck
        # Then it needs to go to the bin stack
        # TODO: Make sure that the flag is unset by the binstack once the card is placed on the bin stack
        if transferred_card.from_player == self.is_player and \
               transferred_card.from_stack_name == Stacks.REMAINDER and\
               transferred_card.from_stack_owner == self.is_player:
            PlayersGameState.set_player_flag(self.is_player, GameStates.Player.PLAYER_BINS_REMAINDER_CARD)
            return True

        return False
    