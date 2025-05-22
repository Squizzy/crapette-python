import socket
import time
from icecream import ic

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
        ic("socket closed")

    def start_server(self):
        self._server_socket.listen()
        ic("server socket listening")

    def accept_connection(self):
        conn, addr = self._server_socket.accept()
        self._client_socket = conn
        self._client_addr = addr
        self._server_connected = True
        time.sleep(1)
        self._acknowledge("connection accepted")
        ic(f"connected by {self._client_addr}")

    def _acknowledge(self, message: str):
        ic(f"acknowledging {message}")
        self._client_socket.sendall(message.encode())
        
    def close_connection(self):
        self._server_connected = False
        self._client_socket.close()
        print("Client disconnected")
        
    def _recv_data(self)  -> bytes:
        # with self._client_socket:
        while True:
            data = self._client_socket.recv(1024)
            if not data:
                break
            print(f"Server received {data!r}")
            # self._client_socket.sendall(data)
            return data

    def listen_for_requests(self):
        ic("listening for requests")
        while self._server_connected:
            data = self._recv_data()
            if data == b"get_player_id":
                self._send_player_id()
            elif data == b"get_stacks_cards 1":
                self._send_stacks_cards()
            elif data == b"quit":
                self._acknowledge("quit accepted")
                self.close_connection()
                
    def _send_player_id(self):
        ic("sending player id")
        self._client_socket.sendall(b"1")

    def _send_stacks_cards(self):
        ic("sending stacks cards")
        self._client_socket.sendall(b"stacks_cards")

if __name__ in "__main__":
    nc = ServerConnection()
    nc.start_server()
    nc.accept_connection()
    nc.listen_for_requests()
    print("123")
