import socket
from abc import ABC, abstractmethod
# from json import loads

# from network_messages import ClientNetworkMessage
from game_logger import GameLogger
# from constants import Players
# from message_decoder import decode_player_id


client_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="client_network: ")
# def log_message(message: str):
#     # enable debug messages
#     DEBUG = True
#     if DEBUG:
#         ic(message)
#         client_logger.debug(message)


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
    
    
    
    def __init__(self, logger: GameLogger, server_ip:str = "127.0.0.1", server_port: int=65432) -> None:
        global client_logger 
        client_logger = logger
        
        self._server_ip = server_ip
        self._server_port = server_port
        self._is_connected = False
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_logger.info("client socket initialised")

    # def __del__(self):
    #     # shut down the sockets so all connections are closed
    #     # self._client_socket.shutdown(socket.SHUT_RDWR)
    #     # close the socket to deallocate it
    #     self._client_socket.close()
    #     # log_message("client socket closed")

    def connect(self) -> None:
        """
        Connect to the server
        Send a connection request to the server 
        
        Returns:
            Nothing
        """
        
        client_logger.info("client connecting to server")
        
        if self._is_connected:
            client_logger.info("client already connected, nothing to do")
            return

        else:        
            # log_message("requesting connection")
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
        self._client_socket.shutdown()
        self._client_socket.close()
        self._is_connected = False
        client_logger.info("client disconnected")

    def send_message(self, message: str) -> None:
    # def send_message(self, client: Players, message: str) -> None:
        """
        Send a message to the server
        """

        client_logger.info("client sending message to server")
        # log_message(f"{client.name} sending message to server")

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
            data = self._client_socket.recv(1024)
            if not data:
                raise ConnectionError("client received no data")
            received_message: str = data.decode()
        except ConnectionError as e:
            raise ConnectionError(f"Failed to receive message from server: {e}")

        client_logger.debug(f"player data received length: {len(received_message)}")
        # log_message(f"receive_message: {self._player_id} data received: {len(received_message)=}")
        
        return received_message

    def is_connected(self) -> bool:
        """
        Check if the client is connected to the server
        """
        return self._is_connected



    # def _send(self, data: str):
    #     """
    #     Send data to the server. 
    #     Data needs to be a string (ideally json encoded)

    #     Args:
    #         data (str): text content to transfer
    #     """
        
    #     client_logger.debug("sending data")
    #     self._client_socket.sendall(data.encode())
    #     log_message("_send: data sent")

    # def _send_request(self, message: ClientNetworkMessage) -> None:
    #     """
    #     Send a request to the server.
    #     Data is a ClientNetworkMessage object
    #     """
        
    #     log_message(f"_send_request {message}: {message.name}")
    #     self._client_socket.sendall(message.name.encode())
    #     log_message("_send_request sent")

    # def _recv(self, max_buffer_size: int) -> str:
    #     """
    #     Receives data from the server and returns it as a string (maybe json encoded?).

    #     Args:
    #         max_buffer_size (int): maximum buffer size in bytees to receive data

    #     Returns:
    #         str: the received data in string format
    #     """
    #     log_message("_recv: client receiving data")
    #     data: bytes = b""
    #     received_message: str = ""
    #     data = self._client_socket.recv(max_buffer_size)
    #     received_message = data.decode()
    #     # while True:
    #     #     data = self._client_socket.recv(max_buffer_size)
    #     #     # ic(f"_recv:client received data: {data.decode()}")
    #     #     if data == b"":
    #     #         if received_message == "":
    #     #             continue
    #     #         else:
    #     #             break
    #     #     else:
    #     #         received_message += data.decode()
         
    #     log_message(f"_recv: client received data finished. {len(received_message)=} received")
    #     # log_message(received_message)
    #     return received_message

    # def request_player_id_from_server(self) -> Players:
    #     """
    #     find out if we are player1 or player2

    #     Returns:
    #         Players: Players.PLAYER1 or 2
    #     """
    #     log_message("request_player_id_from_server: sending request")
        
    #     # message = "send_player_id"
    #     message = ClientNetworkMessage.SEND_PLAYER_ID
    #     self._send_request(message)
        
    #     data: str = self._recv(1024)
    #     # message =  loads(data)
        
    #     # # if data == b"":
    #     # #     log_message("no client player id received")
    #     # #     return None
    #     # # else:
        
    #     # #TODO: Convert to Playsers - maybe even using a dedicated method
    #     # print(type(data))
    #     # self._player_id = int(message)
    #     # log_message(f"client player id received: {self._player_id}")
        
    #     # answer = client_message_decoder.player_id(message)
        
    #     player = decode_player_id(data)
        
    #     # return self._player_id
    #     return player

    # def server_get_stacks_cards(self):
        
    #     log_message("server_get_stacks_cards: client requesting stacks cards")
        
    #     # # empty the current stacks
    #     # self._stacks_cards = []
        
    #     # set the request
    #     self._send_request(ClientNetworkMessage.SEND_STACKS_CARDS)
        
    #     # receive the stacks cards
    #     # TODO: adjust max size sometimes - this is a little bit of an overkill...
    #     data = self._recv(10000)
        
    #     # message = loads(data)

    #     # if the stacks cards are not empty, print the stacks cards
    #     # if len(self._stacks_cards) > 0:
    #     if len(data) >0:
    #         info = loads(data)
    #         log_message(f"client stacks cards received: {info}")
    #     else:
    #         log_message("no client stacks cards received")
            

    # def server_quit(self) -> None:
    #     log_message("server_quit: client quitting")
    #     self.
    #     message = ClientNetworkMessage.QUIT
    #     self._send_request(message)
       
    #     self.disconnect()


if __name__ in "__main__":
    i = 0
    cc = ClientConnection(client_logger)
    cc.connect()
    # for i in range(1):
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    # cc.request_player_id_from_server()
    # cc.server_get_stacks_cards()
    # cc.server_get_stacks_cards()
    # cc.server_get_stacks_cards()
    # cc.server_quit()
    # cc.disconnect()
    # while cc._connected:
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    #     i += 1
    #     if i > 10:
    #         cc._connected = False
