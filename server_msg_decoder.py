from json import loads

from constants import Players
from network_messages import ServerNetworkMessage, ClientNetworkMessage
from game_logger import GameLogger

server_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="message_decoder: ")
# def log_message(message: str):
#     DEBUG = True
#     if DEBUG:
#         ic(message)

class ServerMessageDecoder:
    
    def __init__(self, logger:GameLogger):
        global server_logger
        server_logger = logger

    def decode_request(self, message: str) -> ClientNetworkMessage:
        received_message = loads(message)["type"]
        # server_logger.debug(f"{received_message=}")
        # server_logger.debug(f"{ClientNetworkMessage(received_message)=}")
        # server_logger.debug(f"{ClientNetworkMessage(received_message) == ClientNetworkMessage.SEND_PLAYER_ID}")
        
        return ClientNetworkMessage(received_message)

        