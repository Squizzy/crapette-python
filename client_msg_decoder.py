from json import loads

from constants import Players
from network_messages import ServerNetworkMessage
from game_logger import GameLogger

client_logger: GameLogger
# from icecream import ic # type: ignore
# ic.configureOutput(prefix="message_decoder: ")
# def log_message(message: str):
#     DEBUG = True
#     if DEBUG:
#         ic(message)


class ClientMessageDecoder:

    def __init__(self, logger:GameLogger):
        global client_logger
        client_logger = logger

    def decode_player_id(self, message: str) -> Players:
        client_logger.debug("decoding player_id")
        msg = loads(message)
        client_logger.debug(msg)
        if msg["type"] == ServerNetworkMessage.SENDING_PLAYER_ID.value:
            if msg["target"] == "":
                return Players[msg["value"]]

        else:
            raise ValueError("Incorrect message, no player ID included, or the message was not intended for this player")
        
        return Players.ERROR

    def decode_stacks_cards(self, message: str) -> dict[str, list[str]]:
        received_message = loads(message)
        
        if received_message["type"] == ServerNetworkMessage.SENDING_STACKS_CARDS.value:
            stacks = received_message["value"]
        else:
            client_logger.warning("decode_stacks_cards: problem getting the data")
            
        client_logger.debug(f"decoding_stacks_cards: {stacks=}")
        return {}