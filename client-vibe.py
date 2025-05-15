import socket
import pickle
import threading
from typing import Optional, Callable
from player import Players

class GameClient:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.player_num: Optional[Players] = None
        self.on_game_state_update: Optional[Callable] = None
        self._running = False
        self._receive_thread: Optional[threading.Thread] = None

    def connect(self):
        """Connect to the game server."""
        try:
            self.socket.connect((self.host, self.port))
            self._running = True
            self._receive_thread = threading.Thread(target=self._receive_messages)
            self._receive_thread.daemon = True
            self._receive_thread.start()
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False

    def _receive_messages(self):
        """Continuously receive messages from the server."""
        while self._running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                self._handle_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        self._running = False
        self.socket.close()

    def _handle_message(self, message: dict):
        """Handle incoming messages from the server."""
        if message['type'] == 'player_assignment':
            self.player_num = Players(message['player'])
            print(f"Assigned as Player {self.player_num.value}")
        elif message['type'] == 'game_state':
            if self.on_game_state_update:
                self.on_game_state_update(message)

    def send_move(self, move_data: dict):
        """Send a move to the server."""
        try:
            message = {
                'type': 'move',
                'player': self.player_num.value,
                'data': move_data
            }
            self.socket.sendall(pickle.dumps(message))
        except Exception as e:
            print(f"Error sending move: {e}")

    def request_game_state(self):
        """Request the current game state from the server."""
        try:
            message = {'type': 'game_state_request'}
            self.socket.sendall(pickle.dumps(message))
        except Exception as e:
            print(f"Error requesting game state: {e}")

    def disconnect(self):
        """Disconnect from the server."""
        self._running = False
        if self._receive_thread:
            self._receive_thread.join()
        self.socket.close()

if __name__ == "__main__":
    # Example usage
    client = GameClient()
    if client.connect():
        print("Connected to server!")
        # Example of setting up a game state update handler
        def on_game_state_update(state):
            print(f"Game state updated: {state}")
        client.on_game_state_update = on_game_state_update
        
        try:
            while True:
                # Example of sending a move
                move = input("Enter your move (or 'quit' to exit): ")
                if move.lower() == 'quit':
                    break
                client.send_move({'move': move})
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        finally:
            client.disconnect() 