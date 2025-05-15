import sys
sys.path.append('..')
sys.path.append('.')

from server_network import ServerConnection

def test_initiate_connection():
    nc = ServerConnection()
    assert nc._server_ip == "127.0.0.1"
    assert nc._server_port == 65432
    nc.__del__()
