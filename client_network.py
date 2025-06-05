import socket
import time
from icecream import ic # type: ignore

# enable debug messages
DEBUG = True

def log_message(message: str):
    if DEBUG:
        ic(f"pygame-client: {message}")

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
        self._client_socket.close()
        log_message("client socket closed")

    def connect(self) -> bool:
        """Connect to the server
        Send a connection request to the server 
        wait for an ack from the server 
        
        Returns:
            True if the connection is successful, False otherwise.
        """
        
        log_message("client connecting to server")
        
        if self._connected:
            log_message("client already connected")

        else:        
            self._client_socket.connect((self._server_ip, self._server_port))
            # self._recv_connection_ack()
            log_message("client waiting for connection ack")
            ack:bool | None = self._receive_ack("connection accepted")
            if ack:
                log_message("client connected")
                self._connected = True
            elif ack is False:
                log_message("client not connected")
                self._connected = False
            else:
                print("wrong ack received")
            log_message("client connection ack received")
            
        return self._connected
    # def _recv_connection_ack(self):
    #     data = self._recv(1024)
    #     if data == b"connected":
    #         self._connected = True
    #         ic("client connected ack received")
    #     else:
    #         self._connected = False
    #         ic("client not connected ack not received")
    
    def _receive_ack(self, ack_message) -> bool | None:
        data = self._recv(1024)
        log_message(f"_receive_ack: client received ack data: {data}")
        answer:bool | None = None if data.decode() == "" else \
                             True if data.decode() == ack_message else \
                             False
        return answer
    
    def disconnect(self):
        self._connected = False
        log_message("_disconnect: client disconnected")
        # self._client_socket.sendall(b"hello world")
        # data = self._client_socket.recv(1024)

        # print(f"Client received {data!r}")

    def _send(self, data: bytes):
        log_message("_send: client sending data")
        self._client_socket.sendall(data)

    def _recv(self, size: int):
        log_message("_recv: client receiving data")
        data:bytes = b""
        recvd: list[bytes] = []
        while True:
            data = self._client_socket.recv(size)
            ic(f"_recv:client received data: {recvd}")
            if data == b"":
                break
            return data
        log_message("_recv: client received data finished")

    def server_get_player_id(self) -> int | None:
        log_message("server_get_player_id: client getting player id")
        self._send(b"get_player_id")
        data = self._recv(1024)
        if data == b"":
            log_message("no client player id received")
            return None
        else:
            self._player_id = int(data)
            log_message(f"client player id received: {self._player_id}")
            return self._player_id

    def server_get_stacks_cards(self):
        log_message("server_get_stacks_cards: client requesting stacks cards")
        # empty the current stacks
        self._stacks_cards = []
        # set the message encoded
        message = f"get_stacks_cards {self._player_id}"
        self._send(message.encode())
        
        # receive the stacks information until the server sends an empty message
        while True:
            data = self._recv(1024)
            if data == b"":
                break
            self._stacks_cards.append(data)
            
        # if the stacks cards are not empty, print the stacks cards
        if len(self._stacks_cards) > 0:
            log_message(f"client stacks cards received: {self._stacks_cards}")
        else:
            log_message("no client stacks cards received")

    
    def server_quit(self) -> bool:
        log_message("server_quit: client quitting")
        self._send(b"quit")
        ack:bool | None = self._receive_ack("quit accepted")
        log_message(f"server_quit: client quit ack received: {ack}")
        self.disconnect()
        return self._connected

if __name__ in "__main__":
    i = 0
    cc = ClientConnection()
    cc.connect()
    for i in range(1):
        print('.', end='', flush=True)
        time.sleep(1)
    cc.server_get_player_id()
    cc.server_get_stacks_cards()
    cc.server_get_stacks_cards()
    cc.server_get_stacks_cards()
    cc.server_quit()
    # cc.disconnect()
    # while cc._connected:
    #     print('.', end='', flush=True)
    #     time.sleep(1)
    #     i += 1
    #     if i > 10:
    #         cc._connected = False
