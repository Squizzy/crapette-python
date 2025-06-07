import socket
import pickle
import threading
from typing import Dict, Optional, Callable
from player import Players

class GameServerNetwork:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self._clients: Dict[Players, socket.socket] = {}
        self._lock = threading.Lock()
        self._running = False
        self._on_client_connect: Optional[Callable] = None
        self._on_client_message: Optional[Callable] = None
        
        # Initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)  # Listen for 2 players
        
    def start(self):
        """Start the server and wait for players to connect."""
        self._running = True
        print(f"Server started on {self.server_socket.getsockname()}")
        
        # Wait for two players to connect
        while len(self._clients) < 2 and self._running:
            try:
                client_socket, address = self.server_socket.accept()
                player_num = Players.PLAYER1 if len(self._clients) == 0 else Players.PLAYER2
                self._clients[player_num] = client_socket
                
                # Start a thread to handle messages from this client
                client_thread = threading.Thread(
                    target=self._handle_client_messages,
                    args=(player_num, client_socket)
                )
                client_thread.daemon = True
                client_thread.start()
                
                # Notify about new client connection
                if self._on_client_connect:
                    self._on_client_connect(player_num, address)
                    
                print(f"Player {player_num.value} connected from {address}")
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break
    
    def _handle_client_messages(self, player: Players, client_socket: socket.socket):
        """Handle messages from a specific client."""
        while self._running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                if self._on_client_message:
                    self._on_client_message(player, message)
            except Exception as e:
                print(f"Error handling message from player {player.value}: {e}")
                break
        
        # Clean up when client disconnects
        with self._lock:
            if player in self._clients:
                del self._clients[player]
                client_socket.close()
    
    def send_to_client(self, player: Players, data: dict):
        """Send data to a specific client."""
        with self._lock:
            if player in self._clients:
                try:
                    self._clients[player].sendall(pickle.dumps(data))
                except Exception as e:
                    print(f"Error sending data to player {player.value}: {e}")
    
    def broadcast(self, data: dict):
        """Broadcast data to all connected clients."""
        with self._lock:
            for player in self._clients:
                self.send_to_client(player, data)
    
    def set_on_client_connect(self, callback: Callable[[Players, tuple], None]):
        """Set callback for when a client connects."""
        self._on_client_connect = callback
    
    def set_on_client_message(self, callback: Callable[[Players, dict], None]):
        """Set callback for when a message is received from a client."""
        self._on_client_message = callback
    
    def stop(self):
        """Stop the server and clean up resources."""
        self._running = False
        with self._lock:
            for client in self._clients.values():
                client.close()
            self._clients.clear()
        self.server_socket.close() 