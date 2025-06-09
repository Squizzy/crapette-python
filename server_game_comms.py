from abc import ABC, abstractmethod
from typing import Optional
from server_network import ServerInterface
# import socket

from constants import Players
from message_encoder import encode_player_id, encode_stacks_cards


from icecream import ic # type: ignore
ic.configureOutput(prefix="server_game_comms: ")
def log_message(message: str):
    # enable debug messages
    DEBUG = True
    if DEBUG:
        ic(message)
        
        
class ServerGameCommsInterface(ABC):
    
    @abstractmethod
    def send_player_id(self, player_id: Players) -> None:
        """send the player id to the player"""
        pass
    
    @abstractmethod
    def send_stacks_cards(self, player_id: Players, stacks_cards) -> None:
        """send the current status of all cards in all stacks
        to the player"""
        pass


class ServerGameComms(ServerGameCommsInterface):
    _connection: ServerInterface
    
    def __init__(self, connection) -> None:
        self._connection = connection
    
    def send_player_id(self, player: Players):
        """
        Sends the player_ID to the requesting client
        """
        log_message(f"sending player_id to {player.name}")
        
        message = encode_player_id(player)
        
        self._connection.send_message_to_client(player, message)
        
        log_message("player_id sent")
        
        
    def send_stacks_cards(self, client: Players, stacks_cards):
        log_message("sending stacks cards")
        cards = encode_stacks_cards(stacks_cards)
        # self._client_socket.sendall(b"stacks_cards")
        self._connection.send_message_to_client(client, cards)
        log_message("stacks cards sent")


    def send_players_stacks(self, msg):
        log_message("sending all players stacks cards")
        self._send(msg)
        # self._client_socket.sendall(msg.encode())
        
