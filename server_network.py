import socket
from json import loads, dumps

from constants import Players
from network_messages import server_message_encoder, ServerNetworkMessage, ClientNetworkMessage


from icecream import ic # type: ignore
ic.configureOutput(prefix="server_network: ")
def log_message(message: str):
    # enable debug messages
    DEBUG = True
    if DEBUG:
        ic(message)

class ServerConnection:
    _server_ip: str
    _server_port: int
    _server_socket: socket.socket
    _server_connected: bool
    
    _client_socket: socket.socket
    _client_addr: tuple[str, int]

    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 65432):
        self._server_ip = server_ip
        self._server_port = server_port
        self._server_connected = False
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._server_ip, self._server_port))
        ic("server socket initialised")

    def __del__(self):
        self._server_socket.close()
        # ic("socket closed")

    def start_server(self):
        self._server_socket.listen()
        log_message("server socket listening")

    def accept_connection(self):
        conn, addr = self._server_socket.accept()
        self._client_socket = conn
        self._client_addr = addr
        self._server_connected = True
        # time.sleep(1)
        # self._acknowledge("connection accepted")
        log_message(f"connected by {self._client_addr}")

    # def _acknowledge(self, message: str):
    #     ic(f"acknowledging {message}")
    #     self._client_socket.sendall(message.encode())
        
    def close_connection(self):
        self._server_connected = False
        self._client_socket.close()
        log_message("Client disconnected")
        
    def _recv(self)  -> str:
        
        # with self._client_socket:
        data: bytes = b""
        received_message: str = ""
        
        data = self._client_socket.recv(1024)
        received_message =  data.decode()
        # while True:
        #     data = self._client_socket.recv(1024)
        #     if data == b"":
        #         if received_message == "":
        #             continue
        #         else:
        #             break
        #     else:
                # received_message +=  data.decode()
                
        # ic(f"Received: {received_message}")
        # print(".", end="")
            # print(f"Server received {data!r}")
            # self._client_socket.sendall(data)
        return received_message
        # return b""

    def _send(self, message: str) -> None:
        self._client_socket.sendall(message.encode())


    def listen_for_requests(self):
        log_message("listening for requests")
        while self._server_connected:
            received_message = ""
            received_message = self._recv()

            if received_message == ClientNetworkMessage.SEND_PLAYER_ID.name:
                self._send_player_id(Players.PLAYER1)
                
            elif received_message == ClientNetworkMessage.SEND_STACKS_CARDS.name:
                # self._send_stacks_cards()
                return "send_stacks_cards"
            
            elif received_message == ClientNetworkMessage.QUIT.name:
                # self._acknowledge("quit accepted")
                self.close_connection()
            
            else:
                continue
                
    def _send_player_id(self, player_num:  Players):
        """
        Sending the player ID to the requesting client
        """
        log_message("sending player id")
        
        # player_id = str(0 if player_num == Players.PLAYER1 else 1)
        # ic(player_id)
        # msg = dumps(player_id)
        
        # time.sleep(5)
        # self._client_socket.sendall(msg.encode())
        
        msg = server_message_encoder.player_id(player_num)
        
        self._send(msg)
        
        log_message("player_id sent")
        
    def _send_stacks_cards(self):
        log_message("sending stacks cards")
        self._client_socket.sendall(b"stacks_cards")


    def encoded_msg(self, message) -> str:
        return dumps(message)
    
    def decoded_msg(self, message: str):
        return loads(message)

    def send_players_stacks(self, msg):
        log_message("sending all players stacks cards")
        self._send(msg)
        # self._client_socket.sendall(msg.encode())


if __name__ == "__main__":
    nc = ServerConnection()
    nc.start_server()
    nc.accept_connection()
    nc.listen_for_requests()
