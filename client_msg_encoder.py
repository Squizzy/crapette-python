from json import dumps

# from constants import Players
from network_messages import ClientNetworkMessage
from game_logger import GameLogger

client_logger: GameLogger

# from icecream import ic # type: ignore
# ic.configureOutput(prefix="message_encoder: ")
# def log_message(message: str):
#     DEBUG = True
#     if DEBUG:
#         ic(message)
        
class ClientMessageEncoder:
    def __init__(self, logger: GameLogger):
        global client_logger
        client_logger = logger
        
    def encode_request(self, message: ClientNetworkMessage) -> str:
        msg = {
            "type": message.value,
            "target": "",
            "value": "",
            }
        return dumps(msg)

