import socket
# import time
from constants import Players
from json import loads
from icecream import ic # type: ignore

# enable debug messages
DEBUG = True

ic.configureOutput(prefix="client_network: ")

def log_message(message: str):
    if DEBUG:
        ic(message)
        # ic(f"client_network: {message}")

class ClientConnection:
    # _client_ip: str
    # _client_port: int
    _server_ip: str
    _server_port: int
    _client_socket: socket.socket
    _connected: bool
    _player_id: int
    _stacks_cards: list[bytes]
    
    def __init__(self, server_ip:str = "127.0.0.1", server_port: int=65432) -> None:
        self._server_ip = server_ip
        self._server_port = server_port
        self._connected = False
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log_message("client socket initialised")

    def __del__(self):
        # shut down the sockets so all connections are closed
        # self._client_socket.shutdown(socket.SHUT_RDWR)
        # close the socket to deallocate it
        self._client_socket.close()
        # log_message("client socket closed")

    def connect(self) -> None:
        """
        Connect to the server
        Send a connection request to the server 
        
        Returns:
            Nothing
        """
        
        log_message("client connecting to server")
        
        if self._connected:
            log_message("client already connected")

        else:        
            log_message("requesting connection")
            try:
                self._client_socket.connect((self._server_ip, self._server_port))
            except ConnectionError as e:
                raise ConnectionError(f"Failed to connect to server: {e}")
        
        self._connected = True
        log_message("Connected to server")
        
    def disconnect(self):
        """
        Disconnect from the server
        Probably not strictly necessary? To be checked later
        """
        self.__del__()
        self._connected = False
        log_message("_disconnect: client disconnected")


    def _send(self, data: str):
        """
        Send data to the server. 
        Data needs to be a string (ideally json encoded)

        Args:
            data (str): text content to transfer
        """
        
        log_message("_send: sending data")
        self._client_socket.sendall(data.encode())
        log_message("_send: data sent")

    def _recv(self, max_buffer_size: int) -> str:
        """
        Receives data from the server and returns it as a string (maybe json encoded?).

        Args:
            max_buffer_size (int): maximum buffer size in bytees to receive data

        Returns:
            str: the received data in string format
        """
        log_message("_recv: client receiving data")
        data: bytes = b""
        received_message: str = ""
        data = self._client_socket.recv(max_buffer_size)
        received_message = data.decode()
        # while True:
        #     data = self._client_socket.recv(max_buffer_size)
        #     # ic(f"_recv:client received data: {data.decode()}")
        #     if data == b"":
        #         if received_message == "":
        #             continue
        #         else:
        #             break
        #     else:
        #         received_message += data.decode()
         
        log_message(f"_recv: client received data finished. {len(received_message)=} received")
        # log_message(received_message)
        return received_message

    def request_player_id_from_server(self) -> Players:
        """
        find out if we are player1 or player2

        Returns:
            Players: Players.PLAYER1 or 2
        """
        log_message("request_player_id_from_server: sending request")
        
        message = "send_player_id"
        self._send(message)
        
        data: str = self._recv(1024)
        message =  loads(data)
        
        # if data == b"":
        #     log_message("no client player id received")
        #     return None
        # else:
        
        #TODO: Convert to Playsers - maybe even using a dedicated method
        print(type(data))
        self._player_id = int(message)
        log_message(f"client player id received: {self._player_id}")
        return self._player_id


    def server_get_stacks_cards(self):
        log_message("server_get_stacks_cards: client requesting stacks cards")
        # empty the current stacks
        self._stacks_cards = []
        # set the message encoded
        # message = f"get_stacks_cards {self._player_id}"
        message = "get_stacks_cards"
        # self._send(message.encode())
        self._client_socket.sendall(message.encode())
        log_message(f"requested {message} from server")
        # receive the stacks information until the server sends an empty message
        data = self._recv(10000)
        message = loads(data)
        # data_recieved = False
        # while True:
        #     data = self._client_socket.recv(1024)
        #     # data = self._recv(1024)
        #     if data == b"":
        #         if data_recieved:
        #             break
        #         else:
        #             continue
        #     else:
        #         data_recieved = True
        # print(message)
        # self._stacks_cards.append(data.decode())
            
            # print(data.decode())
            # self._stacks_cards.append(data.decode())
            
        # if the stacks cards are not empty, print the stacks cards
        # if len(self._stacks_cards) > 0:
        if len(message) >0:
            info = loads(data)
            log_message(f"client stacks cards received: {info}")
        else:
            log_message("no client stacks cards received")

    
    def server_quit(self) -> None:
        log_message("server_quit: client quitting")
        message = "quit"
        self._send(message)
       
        self.disconnect()

if __name__ in "__main__":
    i = 0
    cc = ClientConnection()
    cc.connect()
    # for i in range(1):
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    cc.request_player_id_from_server()
    cc.server_get_stacks_cards()
    # cc.server_get_stacks_cards()
    # cc.server_get_stacks_cards()
    cc.server_quit()
    # cc.disconnect()
    # while cc._connected:
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    #     i += 1
    #     if i > 10:
    #         cc._connected = False
