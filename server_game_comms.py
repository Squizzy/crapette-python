from abc import ABC, abstractmethod
from typing import Optional
# import socket

from constants import Players
from server_network import ServerInterface
# from message_encoder import encode_player_id, encode_stacks_cards
from server_msg_encoder import ServerMessageEncoder
from game_logger import GameLogger

server_logger: GameLogger


# from icecream import ic # type: ignore
# ic.configureOutput(prefix="server_game_comms: ")
# def log_message(message: str):
#     # enable debug messages
#     DEBUG = True
#     if DEBUG:
#         ic(message)
        
        
class ServerGameCommsInterface(ABC):
    
    @abstractmethod
    def send_player_id(self, player_id: Players) -> None:
        """send the player id to the player"""
        pass
    
    @abstractmethod
    def send_stacks_cards(self, player_id: Players, stacks_cards: dict[str, list[str]]) -> None:
        """send the current status of all cards in all stacks
        to the player"""
        pass


class ServerGameComms(ServerGameCommsInterface):
    _connection: ServerInterface
    _message_encoder: ServerMessageEncoder
    
    def __init__(self,logger: GameLogger, connection: ServerInterface) -> None:
        global server_logger
        server_logger = logger
        
        self._connection = connection
        
        self._message_encoder = ServerMessageEncoder(logger)
    
    def send_player_id(self, player: Players):
        """
        Sends the player_ID to the requesting client
        """
        server_logger.debug(f"sending player_id to {player.name}")
        
        message = self._message_encoder.encode_player_id(player)
        
        self._connection.send_message_to_client(player, message)
        
        server_logger.info("player_id sent")
        
        
    def send_stacks_cards(self, client: Players, stacks_cards):
        server_logger.info("sending stacks cards")
        cards = self._message_encoder.encode_stacks_cards(stacks_cards)
        self._connection.send_message_to_client(client, cards)
        server_logger.info("stacks cards sent")


    def send_players_stacks(self, msg):
        server_logger.info("sending all players stacks cards")
        # TODO: Complete sending players all stacks
        self._send(msg)
        # self._client_socket.sendall(msg.encode())
        
