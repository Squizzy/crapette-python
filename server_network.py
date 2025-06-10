import socket
from socket import socket as Socket
from abc import ABC, abstractmethod
from typing import Optional

from constants import Players
# from network_messages import ClientNetworkMessage
from game_logger import GameLogger

server_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="server_network: ")
# def log_message(message: str):
#     # enable debug messages
#     DEBUG = True
#     if DEBUG:
#         ic(message)


class ServerInterface(ABC):
    @abstractmethod
    def start(self) -> bool:
        """start the server until it listens for connections"""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """stop the server after all connections are closed"""
        pass
    
    @abstractmethod
    def accept_connection(self) -> bool:
        """Accept a new client connection"""
        pass
    
    @abstractmethod
    def send_message_to_client(self, client: Players, message: str) -> bool:
        """Send a message to connected clients"""
        pass
        
    @abstractmethod
    def receive_message_from_client(self, client: Players) -> str:
        """receive a message from a client"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the server is connected"""
        pass

    @abstractmethod
    def is_player_available(self, player: Players) -> bool:
        """Returns confirmation that the player is available"""
        pass
    
    @property
    @abstractmethod
    def connected_clients(self) -> list[Players]:
        """Returns the connected clients list"""
        pass


class ServerClient:
    _socket: Optional[Socket]
    _address: tuple[str, int]
    _is_connected: bool
    
    def __init__(self):
        self._socket = None
        self._address = ("", -1)
        self._is_connected = False

    @property
    def socket(self) -> Optional[Socket]:
        return self._socket

    @socket.setter
    def socket(self, new_socket: Optional[Socket]) -> None:
        self._socket = new_socket    
        
    @property
    def get_socket_fileno(self) -> int:
        if not self._socket:
            return 0
        return self._socket.fileno()
        
    @property
    def has_socket(self) -> bool:
        return self._socket is not None
        
    @property
    def address(self) -> tuple[str, int]:
        return self._address
    
    @address.setter
    def address(self, this_address: tuple[str, int]) -> None:
        self._address = this_address
        
    @property
    def is_connected(self) -> bool:
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self, connected_state: bool) -> None:
        self._is_connected = connected_state

        
    def _initialise_state(self) -> None:
        # Initialise the client 
        self._socket = None
        self._address = ("", -1)
        self._is_connected = False

    def reset(self) -> None:
        # Disconnect client if connected
        # and reinitialise the variable
        if self._socket:
            try:
                self._socket.close()
                server_logger.debug(f"socket {self._address[0]}:{self._address[1]} closed")
            except socket.error as e:
                server_logger.error(f"Error closing socket {self._address[0]}:{self._address[1]}: {e}")
        self._initialise_state()


class ServerConnection(ServerInterface):
    _server_ip: str
    _server_port: int
    _server_socket: Socket
    _server_connected: bool
    
    # _client_socket: Socket
    # _client_addr: tuple[str, int]
    _clients: dict[Players, ServerClient]
    # _client1: ServerClient
    # _client2: ServerClient

    def __init__(self, logger:  GameLogger, server_ip: str = "127.0.0.1", server_port: int = 65432):
        global server_logger
        server_logger = logger
        
        self._server_ip = server_ip
        self._server_port = server_port
        self._server_connected = False
        self._server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._server_ip, self._server_port))
        server_logger.info("server socket initialised")
        
        self._clients = {}
        self._clients[Players.PLAYER0] = ServerClient()
        self._clients[Players.PLAYER1] = ServerClient()
        server_logger.info("server client slots initialised")

    def __del__(self):
        self._server_socket.close()
        # ic("socket closed")

    def start(self) -> bool:
        try:
            self._server_socket.listen()
            self._server_connected = True
            server_logger.info("server socket listening")
        except socket.error as e:
            server_logger.error(f"Error starting server: {e}")
            return False
        return True
    
    def stop(self) -> None:
        try:
            for client in self._clients:
                self._clients[client].reset()
                # if self._clients[client].is_connected:
                #     self._send_client_disconnection(self._clients[client])
            # if self._client2.is_connected:
            #     self._send_client_disconnection(self._client2)
            self._server_socket.close()
            self._server_connected = False
            server_logger.info("server socket closed")
        except socket.error as e:
            server_logger.error(f"Error stopping server: {e}")

    def accept_connection(self) -> bool:
        this_client_socket: Optional[Socket]
        this_client_address: tuple[str, int]
        this_socket_fileno: int
        
        # accept the socket to start with as it may be a reconnection
        try:
            this_client_socket, this_client_address = self._server_socket.accept()
        except socket.error as e:
            server_logger.error(f"Error accepting connection: {e}")
            return False
        
        this_socket_fileno = this_client_socket.fileno()
        # Check if this is a new proposed connection or an existing one
        if self._clients[Players.PLAYER0].has_socket and \
            self._clients[Players.PLAYER1].has_socket:
            if self._clients[Players.PLAYER0].get_socket_fileno != this_socket_fileno and \
                self._clients[Players.PLAYER1].get_socket_fileno != this_socket_fileno:
                server_logger.warning("Two players already connected, cannot accept a third")
                this_client_socket.close()
                return False

        # Check if this is a reconnection: if the socket number exists 
        # but the client is marked as disconnected 
        # at the same time, cannot have 2 clients with the same socket
        client_to_connect_already_found = False
        for client in self._clients:
            if self._clients[client].get_socket_fileno == this_socket_fileno:
                
                # This should not really ever happen
                if client_to_connect_already_found:
                    this_client_socket.close()
                    raise ValueError("Another player is already connected through this socket")
                
                # Reconnect the client if it is already connected
                # TODO: There may need to be a reconnection notification to provide
                else:
                    self._clients[client].socket = this_client_socket
                    self._clients[client].address = this_client_address
                    self._clients[client].is_connected = True
                    client_to_connect_already_found = True
                    server_logger.debug(f"{client.name} reconnected at {this_client_address}")
                    
        if client_to_connect_already_found:
            return True

        # If this position is reached, it is a new connection and 
        # it is possible as at least one of them is not connected
        for client in self._clients:
            if not self._clients[client].has_socket:
                self._clients[client].socket = this_client_socket
                self._clients[client].address = this_client_address
                self._clients[client].is_connected = True
                server_logger.debug(f"{client.name} connected at {this_client_address}")
                break
        
        return True

    def send_message_to_client(self, client: Players, message: str) -> bool:
        if client not in self._clients:
            server_logger.error("Cannot send message to {client.name}")
            return False
        
        if client in self._clients.keys():
            if not self._clients[client].is_connected:
                server_logger.error(f"{client.name} is not connected, cannot send message")
                return False
        
            if not self._clients[client].socket:
                server_logger.error("Client socket not available, cannot send message")
                return False
        
        if not isinstance(message, str):
            server_logger.error("Message is not a string, cannot send")
            return False
        
        if len(message) > 10000:
            server_logger.error("Message is too large, cannot send")
            return False
        
        try:
            client_socket = self._clients[client].socket
            if client_socket is None:
                server_logger.error("Client socket not available, cannot send message")
                return False
            client_socket.sendall(message.encode())
            # self._clients[client].socket.sendall(message.encode())
        except socket.error as e:
            server_logger.error(f"Error sending message to {client.name}: {e}")
            return False
        
        server_logger.debug(f"sent message: {message} to {client.name}")
        return True

    def receive_message_from_client(self, client:Players) -> str:
        
        if client not in self._clients:
            server_logger.error(f"{client.name} cannot be used to receive messages")
            return ""
        
        if client in self._clients.keys():
            if not self._clients[client].is_connected:
                server_logger.error(f"{client.name} is not connected, cannot receive message from it")
                return ""
            
        received_data: bytes = b""
        
        try:
            client_socket = self._clients[client].socket
            if not client_socket:
                server_logger.error(f"{client.name} has no socket, cannot receive")
                return ""
            received_data = client_socket.recv(1024)
        except socket.error as e:
            server_logger.error(f"Error receiving message from {client.name}: {e}")
            return ""
        
        return received_data.decode()

    # def _send_client_disconnection(self, client: ServerClient):
    #     log_message("sending client disconnection")

    #     msg = ClientNetworkMessage.DISCONNECT.name
    #     self._send(msg)

    #     client.reset()
    #     log_message("client disconnected")

    def is_player_available(self, client: Players) -> bool:
        if client in self._clients:
            if self._clients[client].is_connected:
                return True
        return False

    @property
    def connected_clients(self) -> list[Players]:
        answer = []
        for client in self._clients:
            if self._clients[client].is_connected:
                answer.append(client)
        return answer

    def is_connected(self) -> bool:
        return self._server_connected


#region old ServerConnect methods
    # def start_server(self):
    #     self._server_socket.listen()
    #     log_message("server socket listening")

    # def accept_connection(self):
    #     conn, addr = self._server_socket.accept()
    #     self._client_socket = conn
    #     self._client_addr = addr
    #     self._server_connected = True
    #     # time.sleep(1)
    #     # self._acknowledge("connection accepted")
    #     log_message(f"connected by {self._client_addr}")
    
    # def close_connection(self):
    #     self._server_connected = False
    #     self._client_socket.close()
    #     log_message("Client disconnected")
#endregion

    # def listen_for_requests(self):
    #     log_message("listening for requests")
    #     while self._server_connected:
    #         received_message = ""
    #         received_message = self._recv()

    #         if received_message == ClientNetworkMessage.SEND_PLAYER_ID.name:
    #             self._send_player_id(Players.PLAYER1)
                
    #         elif received_message == ClientNetworkMessage.SEND_STACKS_CARDS.name:
    #             self._send_stacks_cards()
    #             # return "send_stacks_cards"
            
    #         elif received_message == ClientNetworkMessage.QUIT.name:
    #             # self._acknowledge("quit accepted")
    #             self.close_connection()
            
    #         else:
    #             continue
    
            

    
    # def _recv(self)  -> str:
        
    #     # with self._client_socket:
    #     data: bytes = b""
    #     received_message: str = ""
        
    #     data = self._client_socket.recv(1024)
    #     received_message =  data.decode()
    #     # while True:
    #     #     data = self._client_socket.recv(1024)
    #     #     if data == b"":
    #     #         if received_message == "":
    #     #             continue
    #     #         else:
    #     #             break
    #     #     else:
    #             # received_message +=  data.decode()
                
    #     # ic(f"Received: {received_message}")
    #     # print(".", end="")
    #         # print(f"Server received {data!r}")
    #         # self._client_socket.sendall(data)
    #     return received_message
    #     # return b""

    # def _send(self, message: str) -> None:
    #     self._client_socket.sendall(message.encode())


    # def _send_player_id(self, player_num:  Players):
    #     """
    #     Sending the player ID to the requesting client
    #     """
    #     log_message("sending player id")
        
    #     # player_id = str(0 if player_num == Players.PLAYER1 else 1)
    #     # ic(player_id)
    #     # msg = dumps(player_id)
        
    #     # time.sleep(5)
    #     # self._client_socket.sendall(msg.encode())
        
    #     msg = encode_player_id(player_num)
        
    #     self._send(msg)
        
    #     log_message("player_id sent")
        
        
    # def _send_stacks_cards(self):
    #     log_message("sending stacks cards")
        
        
        
    #     self._client_socket.sendall(b"stacks_cards")


    # # def encoded_msg(self, message) -> str:
    # #     return dumps(message)
    
    # # def decoded_msg(self, message: str):
    # #     return loads(message)

    # def send_players_stacks(self, msg):
    #     log_message("sending all players stacks cards")
    #     self._send(msg)
    #     # self._client_socket.sendall(msg.encode())


# if __name__ == "__main__":
#     nc = ServerConnection()
#     nc.start_server()
#     nc.accept_connection()
#     nc.listen_for_requests()
