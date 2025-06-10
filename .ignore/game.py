from player import Player
from constants import Players
from gamestates import GameStates

class Game:
    _player0: Player
    _player1: Player
    _player_turn: Players
    
    
    def __init__(self):
        self._player0 = Player(Players.PLAYER0)
        self._player1 = Player(Players.PLAYER1)
        # TODO: randomise
        self._player_turn = Players.PLAYER0  # Player 1 starts the game
        
        
    @property
    def player_turn(self) -> Players:
        return self._player_turn
        
    def change_turn(self) -> None:
        self._player_turn = Players.PLAYER0 if self._player_turn == Players.PLAYER1 else Players.PLAYER1
        
    def loop(self):
        while True:
            if GameStates.GAME_WON:
                break
            
            if GameStates.Player.PLAYER_BINS_REMAINDER_CARD:
                if self.player_turn == Players.PLAYER0:
                    # self._player1._bin.add_card(Players.PLAYER1, self._player1._remainder)
                    ...
                

if __name__ == "__main__":
    game = Game()