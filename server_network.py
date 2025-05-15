import socket

class ServerConnection:
    _server_ip: str
    _server_port: int
    _server_socket: socket

    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 65432):
        self._server_ip = server_ip
        self._server_port = server_port
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._server_ip, self._server_port))
        self._server_socket.listen()
        print("socket open")
        conn, addr = self._server_socket.accept()
        with conn:
            print(f"connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Server received {data!r}")
                conn.sendall(data)


    def __del__(self):
        self._server_socket.close()
        print("socket closed")


if __name__ in "__main__":
    nc = ServerConnection()
    print("123")
