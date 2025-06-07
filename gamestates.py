from enum import Flag, auto
from constants import Players

# The flags representing the game states

class GameStates(Flag):
    """The various states of the game."""
    # General Game States
    # START = auto()
    # PLAYING = auto()
    # END  = auto()
    GAME_WON =  auto()
    
    # Player-related Stacks States
    class Player(Flag):
        # TODO: If all three below are empty, the player has won the game
        # If set, the crapette stack is empty
        CRAPETTE_IS_EMPTY = auto()  
        # If set, the remainder stack is empty
        REMAINDER_IS_EMPTY = auto()  
        # if set, the bin stack is empty
        BIN_IS_EMPTY =  auto()  
        
        # Communication between remainder stack and bin stack
        # If set, the player has throw its remainder card
        # TODO: the binstack needs to add this card to the bin
        PLAYER_BINS_REMAINDER_CARD = auto()  
        # if set, player has moved the bin cards to the remainder stack
        # TODO: the binstack must empty itself.
        # TODO: the BIN_IS_EMPTY flag needs to be set
        PLAYER_MOVED_BIN_CARDS_TO_REMAINDER = auto() 


# The class maintaining the state of the game for the players.
class PlayersGameState:
    """Maintains the state of the game for the players.
    The class does not need to be instantiated, 
    but it can be used to check the state of the game for a specific player.

    # Raises:
    #     ValueError: _description_
    #     ValueError: _description_
    #     ValueError: _description_
    #     ValueError: _description_
    #     ValueError: _description_

    # Returns:
    #     _type_: _description_
    """
    _player1: GameStates.Player = GameStates.Player(0)
    _player2: GameStates.Player = GameStates.Player(0)

    @classmethod
    def set_player_flag(cls, player_num: Players, flag: GameStates.Player):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Player - player specified incorrect: {player_num}")
        # if flag not in [GameStates.Player.CRAPETTE_IS_EMPTY, GameStates.Player.REMAINDER_IS_EMPTY, GameStates.Player.BIN_IS_EMPTY]:
        #     raise ValueError(f"Error: Problem initiating Player - flag specified incorrect: {flag}")
        if player_num == Players.PLAYER1:
            cls._player1 |= flag
        else:
            cls._player2 |= flag
            
    @classmethod        
    def clear_player_flag(cls, player_num: Players, flag: GameStates.Player):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Player - player specified incorrect: {player_num}")
        # if flag not in [GameStates.Player.CRAPETTE_IS_EMPTY, GameStates.Player.REMAINDER_IS_EMPTY, GameStates.Player.BIN_IS_EMPTY]:
        #     raise ValueError(f"Error: Problem initiating Player - flag specified incorrect: {flag}")
        if player_num == Players.PLAYER1:
            cls._player1 &= ~flag
        else:
            cls._player2 &= ~flag
            
    @classmethod
    def has_game_state(cls, player_num: Players, flag: GameStates.Player):
        if player_num not in [Players.PLAYER1, Players.PLAYER2]:
            raise ValueError(f"Error: Problem initiating Player - player specified incorrect: {player_num}")
        # if flag not in [GameStates.Player1.CRAPETTE_IS_EMPTY, GameStates.Player1.REMAINDER_IS_EMPTY, GameStates.Player1.BIN_IS_EMPTY]:
        #     raise ValueError(f"Error: Problem initiating Player - flag specified incorrect: {flag}") 
        if player_num == Players.PLAYER1:
            return bool(cls._player1 & flag)
        else:
            return bool(cls._player2 & flag)
        
    @classmethod
    def reset_all_flags(cls):
        cls._player1 = GameStates.Player(0)
        cls._player2 = GameStates.Player(0)