import socket
from abc import ABC, abstractmethod

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_network", level=DebugLevel.client_network.value)


class ClientInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Connect to the server"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the server"""
        pass

    @abstractmethod
    def send_message(self, message: str) -> None:
        """Send a message to the server"""
        pass

    @abstractmethod
    def receive_message(self) -> str:
        """Receive a message from the server"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the client is connected to the server"""
        pass


class ClientConnection(ClientInterface):
    _server_ip: str
    _server_port: int
    _client_socket: socket.socket
    _is_connected: bool
    _player_id: int
    _stacks_cards: list[bytes]
    
    def __init__(self, server_ip:str = "127.0.0.1", server_port: int=65432) -> None:
        
        self._server_ip = server_ip
        self._server_port = server_port
        self._is_connected = False
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_logger.info("client socket initialised")


    def connect(self) -> None:
        """
        Connect to the server
        Send a connection request to the server 
        """
        
        client_logger.info("client connecting to server")
        
        if self._is_connected:
            client_logger.info("client already connected, nothing to do")
            return

        else:        
            try:
                self._client_socket.connect((self._server_ip, self._server_port))
            except ConnectionError as e:
                raise ConnectionError(f"Failed to connect to server: {e}")
        
        self._is_connected = True
        client_logger.info("Connected to server")        

    def disconnect(self):
        """
        Disconnect from the server
        Probably not strictly necessary? To be checked later
        """
        # self.__del__()
        # TODO: Announce client disconnection to the server
        self._client_socket.shutdown(socket.SHUT_RDWR)
        self._client_socket.close()
        self._is_connected = False
        client_logger.info("client disconnected")

    def send_message(self, message: str) -> None:
        """
        Send a message to the server
        """

        client_logger.info("client sending message to server")

        try:
            self._client_socket.sendall(message.encode())
        except socket.error as e:
            raise ConnectionError(f"Failed to send message to server: {e}")
        
        client_logger.info("message sent")

    def receive_message(self) -> str:
        """
        Receive a message from the server
        """
        client_logger.info("player receiving message from server")
        # log_message(f"{self._player_id} receiving message from server")
        
        data: bytes = b""
        try:
            data = self._client_socket.recv(1500)
            if not data:
                raise ConnectionError("client received no data")
            received_message: str = data.decode()
        except ConnectionError as e:
            raise ConnectionError(f"Failed to receive message from server: {e}")

        # client_logger.debug(f"player data received length: {len(received_message)}")
        # log_message(f"receive_message: {self._player_id} data received: {len(received_message)=}")
        
        return received_message

    def is_connected(self) -> bool:
        """
        Check if the client is connected to the server
        """
        return self._is_connected


if __name__ in "__main__":
    cc = ClientConnection()
    cc.connect()
    cc.disconnect()

