from constants import Players

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_game_state", level=DebugLevel.client_game_state.value)

# Stores a copy of the game state from the server
# Updates from the server
class GameState:
    _player_id: Players
    _stacks_cards: dict[str, dict[str, list[str]]]
    _is_player0_turn: bool
    _is_running: bool
    
    def __init__(self) -> None:
        self._stacks_cards = {
            "PLAYER0": {
                "crapette":    [],
                "remainder":   [],
                "bin":         [],
                "tableau0":    [],
                "tableau1":    [],
                "tableau2":    [],
                "tableau3":    [],
                "foundation0": [],
                "foundation1": [],
                "foundation2": [],
                "foundation3": [],
            },
            "PLAYER1": {
                "crapette":    [],
                "remainder":   [],
                "bin":         [],
                "tableau0":    [],
                "tableau1":    [],
                "tableau2":    [],
                "tableau3":    [],
                "foundation0": [],
                "foundation1": [],
                "foundation2": [],
                "foundation3": [],
            }
        }
        self._is_running = False
        
    @property
    def player_id(self) -> Players:
        return self._player_id
    
    @player_id.setter
    def player_id(self, player: Players) -> None:
        self._player_id = player
        
    @property
    def stacks_cards(self) -> dict[str, dict[str, list[str]]]:
        return self._stacks_cards
    
    @stacks_cards.setter
    def stacks_cards(self, stacks_cards: dict[str, dict[str, list[str]]]) -> None:
        for player in stacks_cards:
            for stack in stacks_cards[player]:
                for card in stack:
                    self._stacks_cards[player][stack].append(card)
                    
    @property
    def is_player0_turn(self) -> bool:
        return self._is_player0_turn
    
    @is_player0_turn.setter
    def is_player0_turn(self, is_player0_turn: bool) -> None:
        self._is_player0_turn = is_player0_turn