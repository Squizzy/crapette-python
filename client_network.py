import socket

class ClientConnection:
    _client_ip: str
    _client_port: int
    _server_ip: str
    _server_port: int
    _client_socket: socket

    def __init__(self, server_ip:str = "127.0.0.1", server_port: int=65432) -> None:
        self._server_ip = server_ip
        self._server_port = server_port

        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.connect((self._server_ip, self._server_port))
        print("Client connected")
        self._client_socket.sendall(b"hello world")
        data = self._client_socket.recv(1024)

        print(f"Client received {data!r}")

    def __del__(self):
        self._client_socket.close()
        print("Client disconnected")


if __name__ in "__main__":
    cc = ClientConnection()