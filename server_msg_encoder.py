from json import dumps

from constants import Players
from network_messages import ServerNetworkMessage, ClientNetworkMessage
from game_logger import GameLogger

server_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="message_encoder: ")
# def log_message(message: str):
#     DEBUG = True
#     if DEBUG:
#         ic(message)

class ServerMessageEncoder:
    
    def __init__(self, logger: GameLogger) -> None:
        global server_logger
        server_logger = logger

    def encode_request(self, message: ClientNetworkMessage) -> str:
        msg = {
            "type": message.value,
            "target": "",
            "value": "",
            }
        
        return dumps(msg)



    def encode_player_id(self, player: Players) -> str:
        
        server_logger.info("encoding player_id")
        msg = {
            "type": ServerNetworkMessage.SENDING_PLAYER_ID.value,
            #TODO: Implement a message target
            "target": "",
            "value": player.name,
            }
        server_logger.debug(f"{msg}")
        
        return dumps(msg)

    def encode_stacks_cards(self, stacks_cards: dict[str, list[str]]) -> str:
        server_logger.info("encoding stacks_cards")
        msg = {
            "type": ServerNetworkMessage.SENDING_STACKS_CARDS.value,
            "target": "",
            "value": stacks_cards,
            }
        server_logger.debug(f"{msg}")

        return dumps(msg)