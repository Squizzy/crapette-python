from player import Players, Player
from gamestates import GameStates
from server_network import GameServerNetwork
from typing import Optional

class Game:
    def __init__(self):
        self._player1: Optional[Player] = None
        self._player2: Optional[Player] = None
        self._player_turn: Optional[Players] = None
        self._network = GameServerNetwork()
        
        # Set up network callbacks
        self._network.set_on_client_connect(self._handle_client_connect)
        self._network.set_on_client_message(self._handle_client_message)
    
    def start(self):
        """Start the game server."""
        try:
            self._network.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self._network.stop()
    
    def _handle_client_connect(self, player_num: Players, address: tuple):
        """Handle new client connections."""
        if player_num == Players.PLAYER1:
            self._player1 = Player(Players.PLAYER1)
        else:
            self._player2 = Player(Players.PLAYER2)
        
        # Send player number to client
        self._network.send_to_client(player_num, {
            'type': 'player_assignment',
            'player': player_num.value
        })
        
        # Start game when both players are connected
        if self._player1 and self._player2:
            self._player_turn = Players.PLAYER1
            self._broadcast_game_state()
    
    def _handle_client_message(self, player: Players, message: dict):
        """Handle incoming messages from clients."""
        if message['type'] == 'move':
            # Handle player moves here
            # You'll need to implement the game logic for handling moves
            pass
        elif message['type'] == 'game_state_request':
            self._send_game_state(player)
    
    def _send_game_state(self, player: Players):
        """Send current game state to a specific player."""
        self._network.send_to_client(player, {
            'type': 'game_state',
            'current_turn': self._player_turn.value,
            'player1_state': self._player1.get_state() if self._player1 else None,
            'player2_state': self._player2.get_state() if self._player2 else None
        })
    
    def _broadcast_game_state(self):
        """Broadcast current game state to all clients."""
        self._network.broadcast({
            'type': 'game_state',
            'current_turn': self._player_turn.value,
            'player1_state': self._player1.get_state() if self._player1 else None,
            'player2_state': self._player2.get_state() if self._player2 else None
        })

if __name__ == "__main__":
    game = Game()
    game.start()